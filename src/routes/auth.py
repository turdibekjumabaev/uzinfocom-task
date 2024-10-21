from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from src.models import User, OTP, Role
from src.dp import db
import logging

auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    user_role = Role.query.filter_by(role_name='USER').first()

    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    mobile_phone = data.get('mobile_phone')
    otp_code = data.get('otp_code')

    if not mobile_phone or not otp_code or not first_name or not last_name:
        return jsonify({'message': 'All arguments are required'}), 400

    otp = OTP.query.filter_by(phone=mobile_phone).first()

    if not otp:
        return jsonify({'message': 'OTP code not found for this mobile number'}), 400

    if not otp.check_otp(otp_code):
        return jsonify({'message': 'Invalid OTP code'}), 400

    if otp.is_expired() or otp.used:
        return jsonify({'message': 'OTP code expired'}), 400

    user = User.query.filter_by(mobile_phone=mobile_phone).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(first_name=first_name, last_name=last_name, mobile_phone=mobile_phone, role_id=user_role.role_id)
    db.session.add(new_user)
    db.session.commit()

    logger.info(f'Created new user: {new_user.first_name} {new_user.last_name}, Phone: {new_user.mobile_phone}')

    return jsonify({'message': 'User created', 'user_id': new_user.user_id}), 201


@auth_bp.route('/login', methods=['POST'])
def log_in():
    data = request.get_json()
    mobile_phone = data.get('mobile_phone', None)
    otp_code = data.get('otp_code', None)

    if not mobile_phone or not otp_code:
        return jsonify({'message': 'All arguments are required'}), 400

    user = User.query.filter_by(mobile_phone=mobile_phone).first()
    if not user:
        return jsonify({'message': 'User does not exist'}), 400

    otp = OTP.query.filter_by(phone=mobile_phone).first()

    if not otp:
        return jsonify({'message': 'OTP code not found for this mobile number'}), 400

    if not otp.check_otp(otp_code):
        db.session.rollback()
        return jsonify({'message': 'Invalid OTP code'}), 400

    if otp.is_expired() or otp.used:
        return jsonify({'message': 'OTP code expired'}), 400

    access_token = create_access_token(identity=user.mobile_phone)
    logger.info(f'User logged in: {user.first_name} {user.last_name}, Phone: {user.mobile_phone}')

    return jsonify({
        'access_token': access_token,
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name
    }), 200
