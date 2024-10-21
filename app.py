from flask import Flask
from flask_jwt_extended import JWTManager

from src.loader import init_app
from src.services.worker import process_sms

import threading

app = Flask(__name__)
jwt = JWTManager(app)
init_app(app)


def start_worker():
    worker = threading.Thread(target=lambda: process_sms(app))
    worker.start()


if __name__ == "__main__":
    start_worker()
    app.run(port=8080)
