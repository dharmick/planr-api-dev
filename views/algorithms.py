from flask import Blueprint, request, jsonify, current_app as app
from database import db
from authentication import token_required
from algorithms.matrix_factorization.matrix_factorization import run_matrix_factorization
from algorithms.pbdfs.pbdfs import get_pbdfs_schedule
from database import mongodb
import copy
import requests
import numpy as np
from pprint import pprint
import traceback


algorithms_bp = Blueprint('algorithms_bp', __name__)


# =====================================
#     GENERATE MATRIX FACTORIZATION
# =====================================

@algorithms_bp.route('/generate/matrix_factorization', methods=['GET'])
# @token_required
def generate_matrix_factorization():

    user_ratings_from_db = db.session.execute(
        "SELECT * FROM user_ratings"
    )

    no_of_users = db.session.execute(
        "SELECT COUNT(DISTINCT user_id) FROM user_ratings"
    ).scalar()

    no_of_pois = db.session.execute(
        "SELECT COUNT(DISTINCT poi_id) FROM user_ratings"
    ).scalar()

    user_row_map = {}
    poi_column_map = {}
    poi_city_map = {}

    row_index = 0
    column_index = 0

    user_ratings = np.zeros((no_of_users, no_of_pois), dtype=float)

    for rating in user_ratings_from_db:
        if rating.user_id not in user_row_map:
            user_row_map[rating.user_id] = row_index
            row_index += 1
        if rating.poi_id not in poi_column_map:
            poi_column_map[rating.poi_id] = column_index
            column_index += 1
            if rating.city_id in poi_city_map:
                poi_city_map[rating.city_id].append(rating.poi_id)
            else:
                poi_city_map[rating.city_id] = [rating.poi_id]
        user_ratings[user_row_map[rating.user_id]][poi_column_map[rating.poi_id]] = rating.rating


    rui_star = run_matrix_factorization(user_ratings)

    list_to_insert = []
    for user in user_row_map.keys():
        for city in poi_city_map.keys():
            temp = {}
            for poi in poi_city_map[city]:
                temp[str(poi)] = rui_star[user_row_map[user]][poi_column_map[poi]]
            obj = {
                'user_id': user,
                'city_id': city,
                'expected_rating': copy.copy(temp)
            }
            list_to_insert.append(copy.copy(obj))


    mongodb['expected_ratings'].drop()
    x = mongodb['expected_ratings'].insert_many(list_to_insert)
    print(x.inserted_ids)
    return jsonify({
        'message': "done"
    })





# ============================
#     GENERATE PBDFS SCHEDULE
# ============================

@algorithms_bp.route('/generate/pbdfs', methods=['GET'])
@token_required
def generate_pbdfs_schedule(current_user):
    try:
        data = request.args
        city_id = data['city_id']
        source_lat = data['source_lat']
        source_lon = data['source_lon']
        destination_lat = data['destination_lat']
        destination_lon = data['destination_lon']
        departure_time = float(data['departure_time'])
        time_budget = float(data['time_budget'])
        pois_exclude = data['pois_exclude']


        expected_ratings_from_db = mongodb['expected_ratings'].find_one({
            'city_id': int(city_id),
            'user_id': current_user.id
        }, {
            'expected_rating': 1,
            '_id': 0
        })['expected_rating']



        distance_matrix_from_db = mongodb['distance_matrix'].find_one({
            'city_id': city_id
        })['distances']


############################

        url_list = ["http://router.project-osrm.org/table/v1/driving/"]


        pois = list(db.session.execute(
            "SELECT id, latitude, longitude, opening_time, closing_time, time_to_spend, category, name, average_rating FROM pois WHERE city_id = :city_id",
            {
                'city_id': city_id
            }
        ))

        url_list.append(str(source_lon))
        url_list.append(',')
        url_list.append(str(source_lat))
        url_list.append(';')

        url_list.append(str(destination_lon))
        url_list.append(',')
        url_list.append(str(destination_lat))
        url_list.append(';')

        for poi in pois:
            url_list.append(str(poi.longitude))
            url_list.append(',')
            url_list.append(str(poi.latitude))
            url_list.append(';')

        if len(url_list) != 1:
            url_list.pop()
            url = ''.join(url_list)

            try:

                from_source_res = requests.get(url=url, params={'sources': '0'})
                from_source_data = from_source_res.json()

                towards_destination_res = requests.get(url=url, params={'destinations': '1'})
                towards_destination_data = towards_destination_res.json()

            except:
                return jsonify({
                    'message': 'OSRM request unsuccessfull'
                }), 500
            

            
            # print(data)
            if from_source_res and towards_destination_res:
                # source is -1 and destination is -2
                distance_matrix_from_db['-1'] = {}
                distance_matrix_from_db['-2'] = {}

                distance_matrix_from_db['-1']['-1'] = from_source_data['durations'][0][0]/3600
                distance_matrix_from_db['-1']['-2'] = from_source_data['durations'][0][1]/3600
                ind = 2
                for poi in pois:
                    distance_matrix_from_db['-1'][str(poi.id)] = from_source_data['durations'][0][ind]/3600
                    ind += 1


                distance_matrix_from_db['-1']['-2'] = towards_destination_data['durations'][0][0]/3600
                distance_matrix_from_db['-2']['-2'] = towards_destination_data['durations'][1][0]/3600
                ind = 2
                # print(distance_matrix_from_db['144'])
                for poi in pois:
                    distance_matrix_from_db[str(poi.id)]['-2'] = towards_destination_data['durations'][ind][0]/3600
                    ind += 1

                # return jsonify(distance_matrix_from_db)

            else:
                return jsonify({
                    'from source': from_source_data,
                    'towards destination': towards_destination_data,
                    'message': 'OSRM no data found'
                }), 500




###############################



        # pprint(distance_matrix_from_db)

        pois_from_db = db.session.execute(
            "SELECT id, latitude, longitude, opening_time, closing_time, time_to_spend, category, name, average_rating FROM pois WHERE city_id = :city_id",
            {
                'city_id': city_id
            }
        )


        pois_input = {}
        expected_ratings = {}
        for poi in pois_from_db:
            is_percent_match_available = False

            if str(poi.id) not in pois_exclude:
                if str(poi.id) not in expected_ratings_from_db:
                    expected_ratings[str(poi.id)] = poi.average_rating
                else:
                    expected_ratings[str(poi.id)] = expected_ratings_from_db[str(poi.id)]
                    is_percent_match_available = True
                pois_input[str(poi.id)] = {
                    'latitude': poi.latitude,
                    'longitude': poi.longitude,
                    'opening_time': poi.opening_time,
                    'closing_time': poi.closing_time,
                    'time_to_spend': poi.time_to_spend,
                    'category': poi.category,
                    'name': poi.name,
                    'average_rating': poi.average_rating,
                    'is_percent_match_available': is_percent_match_available
                }

        pois_input['-1'] = {
            'time_to_spend': 0,
            'name': 'Source',
            'latitude': source_lat,
            'longitude': source_lon,
            'is_percent_match_available': False,
        }

        pois_input['-2'] = {
            'time_to_spend': 0,
            'name': 'Destination',
            'latitude': destination_lat,
            'longitude': destination_lon,
            'is_percent_match_available': False,
        }


        schedule = get_pbdfs_schedule(
            user_ratings = expected_ratings,
            pois = pois_input,
            source = '-1',
            destination = '-2',
            departure_time = departure_time,
            time_budget = time_budget,
            distance_matrix = distance_matrix_from_db
        )
        # schedule = {}

        db.session.commit()

        return jsonify({
            'success': True,
            'data': schedule
        })

    except Exception as e:
        print("Hii", e)
        traceback.print_exc()
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Something went wrong."
        }), 500

    finally:
        db.session.close()





# ============================
#     GENERATE DISTANCE MATRIX
# ============================

@algorithms_bp.route('/generate/distance_matrix', methods=['GET'])
# @token_required
def generate_distance_matrix():
    cities = db.session.execute(
        "SELECT id FROM cities"
    )

    list_to_insert = []
    for city in cities:
        # print("citty id ", city.id)
        pois  = list(db.session.execute(
            "SELECT id, latitude, longitude FROM pois WHERE city_id = :city_id  ",
            {
                'city_id': city.id
            }
        ))

        url_list = ["http://router.project-osrm.org/table/v1/driving/"]

        for poi in pois:
            url_list.append(str(poi.longitude))
            url_list.append(',')
            url_list.append(str(poi.latitude))
            url_list.append(';')

        if len(url_list) != 1:
            url_list.pop()
            url = ''.join(url_list)

            res = requests.get(url=url)
            data = res.json()
            # print(data)
            if res:
                obj = {
                    'city_id': str(city.id)
                }
                distances = {}

                idx_from=0
                for poi_from in pois:
                    distances[str(poi_from.id)] = {}
                    idx_to = 0
                    for poi_to in pois:
                        distances[str(poi_from.id)][str(poi_to.id)] = data['durations'][idx_from][idx_to]/3600
                        idx_to += 1
                    idx_from += 1

                # print("distances is ", distances)
                obj['distances'] = copy.copy(distances)
                list_to_insert.append(copy.copy(obj))
            else:
                return jsonify(data), 429

    mongodb['distance_matrix'].drop()
    mongodb['distance_matrix'].insert_many(list_to_insert)
    return jsonify({
        "message": "completed succesfully"
    })