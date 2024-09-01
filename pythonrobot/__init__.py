from flask import Flask
# from flask_restful import Api
from pythonrobot.apis import register, test1, test2, cloud_server,local_server
from pythonrobot.util.util import register_log


def create_app():
    app = Flask(__name__)
    app.register_blueprint(register.rs)
    app.register_blueprint(cloud_server.cls)
    app.register_blueprint(local_server.ls)
    app.register_blueprint(test1.ts1)
    app.register_blueprint(test2.ts2)
    register_log(app)
    # api = Api(app)
    return app


