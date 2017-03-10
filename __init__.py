from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from nav import nav
from flask_uploads import UploadSet, AUDIO, configure_uploads

app = Flask(__name__)

wavs = UploadSet('wavs', AUDIO)

from frontend import frontend
from backend import backend


def create_app(configfile=None):
    AppConfig(app)
    Bootstrap(app)
    app.config['UPLOADED_AUDIO_DEST'] = 'songbird/static/uploads'
    app.config['UPLOADS_DEFAULT_DEST'] = 'songbird/static/uploads'
    app.config['UPLOADED_AUDIO_URL'] = 'http://localhost:5000/static/uploads/'
    app.config['UPLOADS_DEFAULT_URL'] = 'http://localhost:5000/static/uploads/'
    configure_uploads(app, wavs)
    app.register_blueprint(frontend)
    app.register_blueprint(backend)
    nav.init_app(app)
    return app