# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables from .env if running locally
    load_dotenv()

    app = Flask(__name__)

    # Secret key for sessions — fallback to dev-safe value
    app.secret_key = os.getenv("SECRET_KEY", "development-placeholder-key")

    # Upload folder for IP input files (ensure directory exists)
    upload_path = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_path, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_path

    # Register main blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app