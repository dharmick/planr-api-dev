from flask import Blueprint, jsonify, request
from authentication import token_required
from database import db
from models import UserRatings
from models import WishlistPlace
from models import WishlistCity
from models import Cities
from models import Pois
general_bp = Blueprint('general_bp', __name__)
import math


# ========================
#   GET ALL CITIES
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

# =====================
#   GET CITY DETAILS
# =====================
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

        isWishlisted_from_db = WishlistCity.query.filter_by(user_id = current_user.id, city_id = city_id).first()

        if isWishlisted_from_db:
            # print("from if")
            isWishlisted = isWishlisted_from_db.value
        else:
            isWishlisted = False
            # print("from else")

        data['isWishlisted'] = isWishlisted

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

        if sum == 0 or total_ratings_count == 0:
            	avg = 0
        else:
        	avg = sum/total_ratings_count
        	avg = int(math.ceil(avg*10)) / 10

        data['ratings'] = {
            'total_count': total_ratings_count,
            'average': avg,
            'individual_ratings': ratings
        }

        pois = db.session.execute("""
            SELECT id, name, image FROM pois WHERE city_id = :city_id
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

# ========================
#   GET POI DETAILS API
# ========================
@general_bp.route('/getPoI', methods=['GET'])
@token_required
def get_PoI(current_user):
    try:
        params = request.args
        poi_id = params['poi_id']

        poi = db.session.execute(
            "SELECT id, name, description, image, opening_time, closing_time,time_to_spend FROM pois WHERE id = :poi_id", {
                "poi_id": poi_id
            }
        ).first()

        if not poi:
            return jsonify({
                "success": False,
                "message": 'Place is not available'
            })

        data = dict(poi)

        isWishlisted_from_db = WishlistPlace.query.filter_by(user_id = current_user.id, poi_id = poi_id).first()

        if isWishlisted_from_db:
            # print("from if")
            isWishlisted = isWishlisted_from_db.value
        else:
            isWishlisted = False
            # print("from else")

        data['isWishlisted'] = isWishlisted

        ratings_from_db = db.session.execute("""
            SELECT rating, count(rating)
            FROM user_ratings WHERE poi_id = :poi_id
            GROUP BY rating
        """, {
            "poi_id": poi_id
        }).fetchall()

        if not ratings_from_db:
            row = db.session.execute(
            "SELECT average_rating FROM pois WHERE id = :poi_id", {
                "poi_id": poi_id
            }
            ).fetchone()

            total_ratings_count = 0
            sum = 0
            # ratings = [
            # 	{
            #         "rating": 1,
            #         "count": 1000
            #     },
            #     {
            #         "rating": 2,
            #         "count": 1500
            #     },
            #     {
            #         "rating": 3,
            #         "count": 100
            #     },
            #     {
            #         "rating": 4,
            #         "count": 10
            #     },
            #     {
            #         "rating": 5,
            #         "count": 5000
            #     }
            # ]

            data['ratings'] = {
                'total_count': total_ratings_count,
                'average': row['average_rating'],
                'individual_ratings': []
            }

        else:
            total_ratings_count = 0
            sum = 0
            ratings = []
            for row in ratings_from_db:
                sum += row.rating * row.count
                total_ratings_count += row.count
                ratings.append(dict(row))

            if sum == 0:
            	avg = 0
            else:
            	avg = sum/total_ratings_count
            	avg = int(math.ceil(avg*10)) / 10

            data['ratings'] = {
                'total_count': total_ratings_count,
                'average': avg,
                'individual_ratings': ratings,
            }

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

# =========================
#   POST USER RATINGS API
# =========================
@general_bp.route('/user-ratings',methods=['GET'])
@token_required
def getuserratings(current_user):
    try:
        params = request.args

        ratings_from_db = UserRatings.query.filter_by(user_id = current_user.id, poi_id = params['poi_id']).first()

        if not ratings_from_db:
            # print("No ratings found")

            new_rating = UserRatings(
            rating =  params['rating'],
            user_id = current_user.id,
            poi_id = params['poi_id'],
            city_id = params['city_id']
            )

            db.session.add(new_rating)
            db.session.commit()

            return jsonify(
                {
                    'success': True,
                    'message': 'New Rating added Successfully'
                }
            )

        else:
            # print("Ratings Updated Successfully")
            ratings_from_db.rating = params['rating']
            db.session.commit()

            return jsonify(
                {
                    'success': True,
                    'message': 'Rating Updated Successfully!'
                }
            )

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Something went wrong.",
        })

    finally:
        db.session.close()


# ======================
#   GET USER RATINGS API
# ======================
@general_bp.route('/getRatings', methods=['GET'])
@token_required
def getRatings(current_user):
	try:
		params = request.args

		user = UserRatings.query.filter_by(user_id = current_user.id, poi_id = params['poi_id']).first()

		if not user:
			return jsonify(
				{
					'success': True,
					'message': 'Rating not available',
					'rating': 0
				}
				)

		else:
			rating = user.rating

			return jsonify(
				{
					'success': True,
					'message': 'Rating available',
					'rating': rating
				}
				)

	except Exception as e:
		print(e)
		return jsonify({
			'success': False,
			'message': 'Something went wrong.',
			})

	finally:
		db.session.close()


# ==============================
#   SEND WISHLISTED ITEM TO DB
# ==============================
@general_bp.route('/wishlist', methods=['POST'])
@token_required
def sendWishlist(current_user):
    try:

        data = request.get_json()

        if 'poi_id' in data:

            wishlist_from_db = WishlistPlace.query.filter_by(user_id = current_user.id, poi_id = data['poi_id']).first()

            if not wishlist_from_db:

                wishlistplace = WishlistPlace(
                    user_id = current_user.id,
                    poi_id = data['poi_id'],
                    value = data['value']
                )

                db.session.add(wishlistplace)
                db.session.commit()

                return jsonify(
                    {
                        'success': True,
                        'message': 'Wishlisted Successfully'
                    }
                )

            else:

                wishlist_from_db.value = data['value']
                db.session.commit()

                return jsonify(
                    {
                        'success': True,
                        'message': 'Wishlist Updated Successfully!'
                    }
                )

        else:

            # print("hii from city")

            wishlist_from_db = WishlistCity.query.filter_by(user_id = current_user.id, city_id = data['city_id']).first()

            if not wishlist_from_db:

                wishlistcity = WishlistCity(
                    user_id = current_user.id,
                    city_id = data['city_id'],
                    value = data['value']
                )

                db.session.add(wishlistcity)
                db.session.commit()

                return jsonify(
                    {
                        'success': True,
                        'message': 'Wishlisted City Successfully'
                    }
                )

            else:

                wishlist_from_db.value = data['value']
                db.session.commit()

                return jsonify(
                    {
                        'success': True,
                        'message': 'Wishlist Updated Successfully!'
                    }
                )

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Something went wrong.",
        })

    finally:
        db.session.close()


# ====================================
#   RECEIVE WISHLISTED ITEM OF A USER
# ====================================
@general_bp.route('/wishlist', methods=['GET'])
@token_required
def getWishlist(current_user):
    try:

        wishlistedPlace = WishlistPlace.query.filter_by(user_id = current_user.id)
        wishlistedCity = WishlistCity.query.filter_by(user_id = current_user.id)

        """wishlist = {
            'pois': [
                {
                    'id': 92,
                    'name':
                    'description':
                    'image':
                    'rating':
                }
            ]
        }"""

        wishlist = {
            'pois': [],
            'cities': []
        }

        for p in wishlistedPlace:
            poi = Pois.query.filter_by(id = p.poi_id).first()
            place = {}
            place['id'] = p.poi_id
            place['name'] = poi.name
            place['description'] = poi.description
            place['image'] = poi.image
            place['rating'] = poi.average_rating
            wishlist['pois'].append(place)

        for c in wishlistedCity:
            city = Cities.query.filter_by(id = c.city_id).first()
            cities = {}
            cities['id'] = c.city_id
            cities['name'] = city.name
            cities['description'] = city.description
            cities['image'] = city.image
            wishlist['cities'].append(cities)

        return jsonify(
                    {
                        'success': True,
                        'wishlist': wishlist,
                        'message': 'Wishlist Displayed Successfully'
                    }
                )

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Something went wrong.",
        })

    finally:
        db.session.close()