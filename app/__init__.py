# Initializes Flask app and loads environment variables
from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    from app.routes import main
    app.register_blueprint(main)

    app.secret_key = os.environ.get("SECRET_KEY", "temp-secret-dev")

    return app