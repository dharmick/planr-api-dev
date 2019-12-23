from flask import Blueprint, request, jsonify, current_app as app
from models import Users
from database import db
from views.authentication import token_required
from algorithms.pbdfs.pbdfs import get_pbdfs_schedule

schedule_bp = Blueprint('schedule_bp', __name__)


# ============================
#     GENERATE PBDFS SCHEDULE
# ============================

@schedule_bp.route('/generate/pbdfs', methods=['GET'])
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

