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
    ).fetchall()

    no_of_users = db.session.execute(
        "SELECT COUNT(DISTINCT user_id) FROM user_ratings"
    ).scalar()

    no_of_pois = db.session.execute(
        "SELECT COUNT(DISTINCT poi_id) FROM user_ratings"
    ).scalar()

    user_row_map = {}
    poi_column_map = {}

    row_index = 0
    column_index = 0

    user_ratings = np.zeros((no_of_users, no_of_pois), dtype=float)

    for row in user_ratings_from_db:
        if row['user_id'] not in user_row_map:
            user_row_map[row['user_id']] = row_index
            row_index += 1
        if row['poi_id'] not in poi_column_map:
            poi_column_map[row['poi_id']] = column_index
            column_index += 1
        user_ratings[user_row_map[row['user_id']]][poi_column_map[row['poi_id']]] = row['rating']


    rui_star = run_matrix_factorization(user_ratings)

    list_to_insert = []
    for user in user_row_map.keys():
        for poi in poi_column_map.keys():
            obj = {
                'user_id': user,
                'poi_id': poi,
                'expected_rating': rui_star[user_row_map[user]][poi_column_map[poi]]
            }
            list_to_insert.append(copy.copy(obj))


    mongodb['expected_ratings'].drop()
    x = mongodb['expected_ratings'].insert_many(list_to_insert)
    # print(x.inserted_ids)
    return jsonify({
        'message': "done"
    })


