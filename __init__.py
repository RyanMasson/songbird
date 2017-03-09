from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from nav import nav
from frontend import frontend

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app)
    Bootstrap(app)
    app.register_blueprint(frontend)
    nav.init_app(app)
    return app