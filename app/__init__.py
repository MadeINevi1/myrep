from flask import Flask
from flask_bootstrap import Bootstrap5
from app.config import Config
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from app.models import get_user_by_id
    return get_user_by_id(int(user_id))

app.config.from_object(Config)

csrf = CSRFProtect(app)

from app import routes
