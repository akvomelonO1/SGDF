import os

from flask import Flask


def create_app(test_config=None):
    # CREATEA AND CONFIG THE APP
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='impossible_key',
        DATABASE=os.path.join(app.instance_path, 'SGDF.sqlite'),
    )

    if test_config is None:
        # LOAD THE INSTANCE CONFIG IF EXISTS AND NOT DURING TESTING
        app.config.from_pyfile('config.py', silent=True)
    else:
        # LOAD THE TEST CONFIG
        app.config.from_mapping(test_config)

    # ENSURE THE FOLDER EXISTS
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    return app