from flask import Flask

app = Flask(__name__)

from flask_cors import CORS

CORS(app)

from app import view
from app import control

from app.model import db
from app.model import database
from app.model.database import Audience, Checkout

from configuration import configs
env = "dev"
app.config.from_object(configs[env])
