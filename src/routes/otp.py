from flask import Blueprint, request, jsonify

from src.models import OTP
from src.dp import db, redis

import logging
import json
import secrets
import re

otp_bp = Blueprint('otp', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_phone(mobile_phone):
    pattern = r"^998(90|91|93|94|95|98|99|33|97|71)\d{7}$"
    return re.match(pattern, mobile_phone)


@otp_bp.route('/send', methods=['POST'])
def otp():
    try:
        data = request.json
        mobile_phone = data.get("mobile_phone", None)

        if mobile_phone is None:
            return jsonify({'message': 'mobile_phone is required'}), 400

        if not validate_phone(mobile_phone):
            return jsonify({'message': 'Invalid mobile_phone format'}), 400

        otp_code = str(secrets.randbelow(9000) + 1000)
        # logger.info(f"Generated OTP code: {otp_code} for mobile_phone: {mobile_phone}")

        existing_otp = OTP.query.filter_by(phone=mobile_phone).first()

        if existing_otp:
            if existing_otp.is_expired():
                # logger.info(f"Updating existing OTP record for mobile_phone: {mobile_phone}")
                existing_otp.used = False
                existing_otp.set_otp(otp_code)
            else:
                return jsonify({'message': 'The OTP given to you is still usable'}), 400
        else:
            logger.info(f"Creating new OTP record for mobile_phone: {mobile_phone}")
            new_otp = OTP(phone=mobile_phone)
            new_otp.set_otp(otp_code)
            db.session.add(new_otp)

        db.session.commit()
        # logger.info(f"OTP saved to database for mobile_phone: {mobile_phone}")

        redis.rpush('sms_queue', json.dumps({
            'mobile_phone': mobile_phone,
            'message': f'Ketti.uz ushın tastıyqlaw kodı: {otp_code}'
        }))
        logger.info(f"OTP code pushed to Redis queue for mobile_phone: {mobile_phone}")

        return jsonify({'message': "The OTP code has been added to the queue"}), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return jsonify({'message': 'Please try again later'}), 500
