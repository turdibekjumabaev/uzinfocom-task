from flask import Flask

from src.loader import init_app

app = Flask(__name__)
init_app(app)


if __name__ == "__main__":
    app.run(port=8080)
