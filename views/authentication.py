from flask import Blueprint, request, jsonify, current_app as app
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps



authentication_bp = Blueprint('authentication_bp', __name__)

from models import Users
from database import db


# ============================
#     CHECK PRESENCE OF TOKEN
# ============================

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authentication')

        if not token:
            return jsonify({
                'message': 'Token missing'
            }), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({
                'message': 'Token invalid',
            }), 401

        return f(current_user, *args, **kwargs)
    return decorated


# ====================
#     USER SIGNUP
# ====================

@authentication_bp.route('/signup', methods=['POST'])
def user_signup():
    data = request.get_json()

    user = Users.query.filter_by(email=data['email']).first()

    if user:
        return jsonify(
            {
                'success': False,
                'message': 'User already exists!'
            }
        )

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(
        public_id=str(uuid.uuid4()),
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        admin=False
    )

    token = jwt.encode(
            {
                'public_id': new_user.public_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            },
            app.config['SECRET_KEY']
        )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        {
            'success': True,
            'message': 'Signup successfull',
            'token': token,
        }
    )


# ====================
#     USER LOGIN
# ====================

@authentication_bp.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()

    user = Users.query.filter_by(email=data['email']).first()

    # user not found
    if not user:
        return jsonify(
            {
                'success': False,
                'message': 'Authentication failed'
            }
        ), 401

    # password matched
    if check_password_hash(user.password, data['password']):
        token = jwt.encode(
            {
                'public_id': user.public_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            app.config['SECRET_KEY']
        )
        return jsonify(
            {
                'success': True,
                'message': 'Login successfull',
                'token': token
            }
        )

    # password not matched
    return jsonify(
        {
            'success': False,
            'message': 'Authentication failed'
        }
    ), 401

