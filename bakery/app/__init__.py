#init

from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "/login"


from app import views
