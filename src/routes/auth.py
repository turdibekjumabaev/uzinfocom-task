from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from src.models import User, OTP, Role
from src.dp import db
import logging

auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
        Jańa paydalanıwshılar dizimnen ótiwi ushın
        ---
        tags:
            - Auth
        parameters:
          - name: body
            in: body
            required: true
            description: JSON object
            schema:
              type: object
              required:
                - first_name
                - last_name
                - mobile_phone
                - otp_code
              properties:
                first_name:
                  type: string
                  description: Paydalanıwshınıń atı
                  example: Turdıbek
                last_name:
                  type: string
                  description: Paydalanıwshınıń familiyası
                  example: Jumabaev
                mobile_phone:
                  type: string
                  description: Telefon nomer
                  example: 998932000573
                otp_code:
                  type: string
                  description: Tastıyıqlaw ushın bir mártelik kod
                  example: 1234
        responses:
          201:
            description: Jańa paydalanıwshı jaratıldı
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User created"
                user_id:
                  type: integer
                  example: 1
          400:
            description: Jańa paydalanıwshı jaratılmaǵan jaǵday
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: ["All arguments are required", "OTP code not found for this mobile number", "User already exists"]
          500:
            description: Qátelik ☠️
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Please try again later"
        """
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

    if otp.is_expired():
        return jsonify({'message': 'OTP code expired'}), 400

    user = User.query.filter_by(mobile_phone=mobile_phone).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(first_name=first_name, last_name=last_name, mobile_phone=mobile_phone, role_id=user_role.role_id)
    otp.mark_as_used()
    db.session.add(new_user)
    db.session.commit()

    logger.info(f'Created new user: {new_user.first_name} {new_user.last_name}, Phone: {new_user.mobile_phone}')

    return jsonify({'message': 'User created', 'user_id': new_user.user_id}), 201


@auth_bp.route('/login', methods=['POST'])
def log_in():
    """
        Júyege kiriw
        ---
        tags:
            - Auth
        parameters:
          - name: body
            in: body
            required: true
            description: JSON object
            schema:
              type: object
              required:
                - mobile_phone
                - otp_code
              properties:
                mobile_phone:
                  type: string
                  description: Telefon nomer
                  example: 998932000573
                otp_code:
                  type: string
                  description: Tastıyıqlaw kodı
                  example: 1234
        responses:
          200:
            description: Tabıslı! Paydalanıwshı ushın access_token jaratıp berildi
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                user_id:
                  type: integer
                  example: 1
                first_name:
                  type: string
                  example: John
                last_name:
                  type: string
                  example: Doe
          400:
            description: Kirgizilgen maǵlıwmatlardaǵı qátelik yamasa jaramsız OTP
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: ["All arguments are required", "User does not exist", "Invalid OTP code"]
          500:
            description: Qátelik ☠️
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Please try again later"
        """
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

    if otp.is_expired():
        return jsonify({'message': 'OTP code expired'}), 400

    access_token = create_access_token(identity=user.mobile_phone)
    logger.info(f'User logged in: {user.first_name} {user.last_name}, Phone: {user.mobile_phone}')

    otp.mark_as_used()
    db.session.commit()

    return jsonify({
        'access_token': access_token,
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name
    }), 200


@auth_bp.route('/register-admin', methods=['POST'])
@jwt_required()
def register_admin():
    """
    Jańa admindi dizimnen ótkeriw
    ---
    tags:
        - Admin Auth
    parameters:
      - name: body
        in: body
        required: true
        description: JSON object
        schema:
          type: object
          required:
            - first_name
            - last_name
            - mobile_phone
            - password
          properties:
            first_name:
              type: string
              description: Atı
              example: Turdıbek
            last_name:
              type: string
              description: Familiyası
              example: Jumabaev
            mobile_phone:
              type: string
              description: Telefon nomer
              example: 998932000573
            password:
              type: string
              description: Parol
              example: <PASSWORD>
    responses:
      200:
        description: Tabıslı! Admin ushın access_token jaratıp berildi
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Admin registered"
      403:
        description: Admin roline iye bolmaǵan paydalanıwshı admin akkount jaratıwǵa háreket etkende
        schema:
          type: object
          properties:
            message:
              type: string
              example: "You are not an admin"

    """
    current_user_phone_number = get_jwt_identity()
    current_user = User.query.filter_by(mobile_phone=current_user_phone_number).first()
    admin_role = Role.query.filter_by(role_name='ADMIN').first()

    if current_user.role_id != admin_role.role_id:
        return jsonify({'message': 'You are not an admin'}), 403

    data = request.get_json()
    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)
    mobile_phone = data.get('mobile_phone', None)
    password = data.get('password', None)

    new_admin = User(first_name=first_name, last_name=last_name, mobile_phone=mobile_phone, password=password, role_id=admin_role.role_id)
    db.session.add(new_admin)
    db.session.commit()
    logger.info(f'Admin registered: {current_user.first_name} {current_user.last_name}')

    return jsonify({'message': 'Admin registered'}), 200


@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    """
    Adminler ushın júyege kiriw
    ---
    tags:
        - Admin Auth
    parameters:
      - name: body
        in: body
        required: true
        description: JSON object
        schema:
          type: object
          required:
            - mobile_phone
            - password
          properties:
            mobile_phone:
              type: string
              description: Telefon nomer
              example: 998932000573
            otp_code:
              type: string
              description: Tastıyıqlaw ushın kod
              example: 1234
    responses:
      200:
        description: Tabıslı! Amdin ushın access_token jaratıp berildi
        schema:
          type: object
          properties:
            access_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            user_id:
              type: integer
              example: 1
            first_name:
              type: string
              example: Turdıbek
            last_name:
              type: string
              example: Jumabaev
      400:
        description: Kirgizilgen maǵlıwmatlarda qátelik
        schema:
          type: object
          properties:
            message:
              type: string
              example: ["All arguments are required", "User does not exist", "Invalid password"]
    """
    data = request.get_json()
    mobile_phone = data.get('mobile_phone', None)
    password = data.get('password', None)

    if not mobile_phone or not password:
        return jsonify({'message': 'All arguments are required'}), 400

    user = User.query.filter_by(mobile_phone=mobile_phone).first()
    if not user:
        return jsonify({'message': 'User does not exist'}), 400

    if not user.check_password(password):
        return jsonify({'message': 'Invalid password'}), 400

    access_token = create_access_token(identity=user.mobile_phone)
    logger.info(f'Admin logged in: {user.first_name} {user.last_name}')

    return jsonify({
        'access_token': access_token,
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name
    }), 200
