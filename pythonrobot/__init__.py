from flask import Flask
from .apis import combine_server,register,test1,test2,cloud_server
def create_app():
    app = Flask(__name__)
    app.register_blueprint(combine_server.cs)
    app.register_blueprint(register.rs)
    app.register_blueprint(cloud_server.cls)
    app.register_blueprint(test1.ts1)
    app.register_blueprint(test2.ts2)
    return app