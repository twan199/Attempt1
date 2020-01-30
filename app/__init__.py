import os
from flask import Flask, redirect
from flask import url_for

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
# Application factory
def create_app():

    app = Flask(__name__, instance_relative_config=True)

    # First, configure from (versioned) default configuration
    from os import environ
    configuration_class_name = environ['APP_CONFIGURATION_CLASS'] if (
        'APP_CONFIGURATION_CLASS' in environ) else None

    from werkzeug.utils import import_string
    configuration_object = import_string(
        configuration_class_name or 'app.defaults.ProductionConfig')()

    app.config.from_object(configuration_object)

    # Second, apply instance configuration,
    # this file is NOT in version control for obvious reasons.
    app.config.from_pyfile('config.py')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()
        from app.upload import blueprint as upload_blueprint

        app.register_blueprint(upload_blueprint, url_prefix='/twan')

        @app.route('/')
        def root():
            return redirect("/twan/static/upload.html", code=302)

        return app