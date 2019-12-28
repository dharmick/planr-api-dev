from flask import Blueprint, request, jsonify, current_app as app
from models import UserRatings
from database import db
from views.authentication import token_required
import numpy as np
from algorithms.matrix_factorization.matrix_factorization import run_matrix_factorization
from database import mongodb
import copy

matrix_factorization_bp = Blueprint('matrix_factorization_bp', __name__)


# ============================
#     GENERATE MATRIX FACTORIZATION
# ============================

@matrix_factorization_bp.route('/generate/matrix_factorization', methods=['GET'])
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
        # list_to_insert[user] = {}
        for city in poi_city_map.keys():
            temp = {}
            for poi in poi_city_map[city]:
                temp[str(poi)] = rui_star[user_row_map[user]][poi_column_map[poi]]

            # list_to_insert[user][poi_city_map[poi]][poi] = rui_star[user_row_map[user]][poi_column_map[poi]]
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


