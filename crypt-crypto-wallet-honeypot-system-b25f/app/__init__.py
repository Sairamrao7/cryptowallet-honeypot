from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///honeypot.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app)

    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    @app.route('/')
    def index():
        return app.send_static_file('index.html') if os.path.exists(os.path.join(app.static_folder, 'index.html')) else app.send_static_file('../templates/index.html')

    return app