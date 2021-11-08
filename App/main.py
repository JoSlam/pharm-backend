from flask import Flask
from flask import session
from datetime import timedelta
from flask_cors import CORS
from flask_jwt_extended import JWTManager


import pyrebase

from App.database import *


from App import CONFIG


from App.controllers.auth import auth_bp
from App.controllers.order import order_bp

from App.views import (
    api_views,
    product_views,
    search_view,
    customer_views
)

# Google Firebase configuration file.
config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId": ""
}


firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

# to store image
# storage.child("image-url-on-firebase").put("image-name.jpg") (png whatever file extension")

# to download image
# storage.child("image-url-on-firebase").download("image-name.jpg")


def create_app():
    app = Flask(__name__, static_url_path='')
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
    app.config['UPLOADED_PHOTOS_DEST'] = 'uploads',

    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG["SQLALCHEMY_DATABASE_URI"]
    app.config['SECRET_KEY'] = CONFIG['SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(
        days=CONFIG["JWT_ACCESS_TOKEN_EXPIRES"])
    app.config['DEBUG'] = CONFIG["DEBUG"]
    #photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    #configure_uploads(app, photos)
    db.init_app(app)
    JWTManager(app)
    return app


app = create_app()

app.app_context().push()

app.register_blueprint(auth_bp)
app.register_blueprint(order_bp)
app.register_blueprint(api_views)
app.register_blueprint(product_views)
app.register_blueprint(search_view)
app.register_blueprint(customer_views)

# jwt = JWT(app, authenticateUser, identityHandler)

if __name__ == '__main__':
    print('Application running in '+CONFIG['ENV']+' mode')
    app.run(host='localhost', port=8080, debug=CONFIG['DEBUG'])
