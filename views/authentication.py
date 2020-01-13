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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
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

# ====================
#     GET ALL USERS
# ====================

@authentication_bp.route('/users', methods = ['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({
            'message': 'Cannot perform that function!'
        })

    users = Users.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
        
    return jsonify({'users': output})

# ====================
#     PASSWORD RESET
# ====================
@authentication_bp.route('/reset-password', methods=['PUT'])
@token_required
def resetpassword(current_user):

    public_id = current_user.public_id

    user = Users.query.filter_by(public_id = public_id).first()

    # user not found
    if not user:
        return jsonify(
            {
                'success': False,
                'message': 'Authentication failed'
            }
        ), 401
    
    data = request.get_json()

    # password matching
    if check_password_hash(user.password, data['password']):
        if data['newpassword'] == data['confirmpassword']:
            hashed_password = generate_password_hash(data['newpassword'], method='sha256')
            user.password = hashed_password
            db.session.commit()
            return jsonify(
                {
                    'success': True,
                    'message': 'Password changed successfully!',
                }
            )
        else:
            return jsonify(
                {
                    'success': False,
                    'message': 'Password did not match. Enter again!',
                }
            )
        
    # password not matched
    return jsonify(
        {
            'success': False,
            'message': 'Please enter correct password!'
        }
    ), 401