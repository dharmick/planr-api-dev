from flask import Blueprint, request, jsonify, current_app as app
from database import db
from views.authentication import token_required
from algorithms.matrix_factorization.matrix_factorization import run_matrix_factorization
from algorithms.pbdfs.pbdfs import get_pbdfs_schedule
from database import mongodb
import copy
import requests
import numpy as np


algorithms_bp = Blueprint('algorithms_bp', __name__)


# ============================
#     GENERATE MATRIX FACTORIZATION
# ============================

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
    data = request.args
    city_id = data['city_id']
    source = data['source']
    destination = data['destination']
    departure_time = data['departure_time']
    time_budget = data['time_budget']


    user_ratings = db.session.execute(
        "SELECT * FROM cities"
    )
    names = [row[0] for row in user_ratings]
    print (names)


    # print(current_user.public_id)

    return jsonify({
        'ratings': current_user.id
    })





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