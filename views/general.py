from flask import Blueprint, jsonify, request
from authentication import token_required
from database import db

general_bp = Blueprint('general_bp', __name__)


# =========================
# GET ALL CITIES
# ========================

@general_bp.route('/getAllCities', methods=['GET'])
@token_required
def get_all_routes(current_user):
    try:
        cities = db.session.execute(
            "SELECT id, name FROM cities"
        ).fetchall()
        data = [ dict(row) for row in cities]
        db.session.commit()
        return jsonify({
            "success": True,
            "data": data
        })
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({
            "message": "something went wrong",
            "success": False
        })
    finally:
        db.session.close()

# =========================
# GET CITY DETAILS
# ========================

@general_bp.route('/getCity', methods=['GET'])
@token_required
def get_city(current_user):
    try:
        params = request.args
        city_id = params['city_id']

        city = db.session.execute(
            "SELECT id, name, description, image FROM cities WHERE id = :city_id", {
                "city_id": city_id
            }
        ).first()

        if not city:
            return jsonify({
                "success": False,
                "message": 'city id not valid'
            })

        data = dict(city)

        ratings_from_db = db.session.execute("""
            SELECT rating, count(rating)
            FROM user_ratings WHERE city_id = :city_id
            GROUP BY rating
        """, {
            "city_id": city_id
        }).fetchall()

        total_ratings_count = 0
        sum = 0
        ratings = []
        for row in ratings_from_db:
            sum += row.rating * row.count
            total_ratings_count += row.count
            ratings.append(dict(row))

        data['ratings'] = {
            'total_count': total_ratings_count,
            'average': 0 if sum == 0 else sum/total_ratings_count,
            'individual_ratings': ratings
        }

        pois = db.session.execute("""
            SELECT id, name FROM pois WHERE city_id = :city_id
        """, {
            'city_id': city_id
        }).fetchall()

        data['pois'] = [dict(row) for row in pois]

        # print(ratings)
        db.session.commit()
        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Something went wrong."
        })

    finally:
        db.session.close()




