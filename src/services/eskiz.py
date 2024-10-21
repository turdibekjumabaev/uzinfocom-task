import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Eskiz:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.base_url = 'https://notify.eskiz.uz'
        self.token = None

    def generate_new_token(self):
        payload = {
            'email': self.email,
            'password': self.password
        }

        response = requests.post(f'{self.base_url}/api/auth/login', data=payload)
        return response.json()

    def set_token(self):
        self.token = self.generate_new_token()['data']['token']

    def refresh_token(self, token=None):
        if token is None:
            self.set_token()

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.post(f'{self.base_url}/api/auth/refresh', headers=headers)
        if response.status_code == 401:
            logger.info(f'Eskiz login or password is incorrect')
        return response.json()

    def send_sms(self, mobile_phone, message):
        if self.token is None:
            self.set_token()

        payload = {
            'mobile_phone': mobile_phone,
            'message': message,
            'from': '4546'
        }
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.post(f'{self.base_url}/api/message/sms/send', data=payload, headers=headers)

        if response.status_code == 200:
            logger.info(f'Eskiz sms sent to {mobile_phone}')
        elif response.status_code == 401:
            logger.error(f'Eskiz authentication failed')
        elif response.status_code == 400:
            logger.error(f'Failed to send sms to {mobile_phone}: {response.json().get("message")}')

        return response
