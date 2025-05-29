import os
import logging
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    from .routes import bp
    app.register_blueprint(bp)

    return app