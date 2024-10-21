from dotenv import load_dotenv

from src.dp import db, redis
from src.services.eskiz import Eskiz

import os
import json
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
eskiz = Eskiz(os.getenv('ESKIZ_EMAIL'), os.getenv('ESKIZ_PASSWORD'))


def send_sms(phone_number, message):
    try:
        response = eskiz.send_sms(phone_number, message)
        if response.status_code == 200:
            logger.info(f"Successfully sent SMS to {phone_number}: {message}")
            return True
        else:
            logger.error(f"Failed to send SMS to {phone_number}: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending SMS to {phone_number}: {e}")
        return False


def update_sms_status(sms, status):
    sms.status = status
    db.session.commit()


def process_sms(app):
    while True:
        sms_data = redis.blpop('sms_queue')
        if sms_data:
            sms_data = json.loads(sms_data[1])
            mobile_phone = sms_data['mobile_phone']
            message = sms_data['message']

            with app.app_context():
                send_sms(mobile_phone, message)
                logger.info(f'"{message}" message sent to {mobile_phone}')
