from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = "yikesss"

bcrypt = Bcrypt(app)


DATABASE = 'login_and_registration'

from flask_app.controllers import controller_user
