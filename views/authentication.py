from flask import Blueprint, request, jsonify
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

authentication_bp = Blueprint('authentication_bp', __name__)

from models import Users
from app import db


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

    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        {
            'success': True,
            'message': 'Signup successfull'
        }
    )


# ====================
#     USER LOGIN
# ====================

