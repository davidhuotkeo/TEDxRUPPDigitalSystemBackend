from flask import Flask

app = Flask(__name__)

from app import view
from app import control

from app.model import db
from app.model import database
from app.model.database import Audience, Checkout

from configuration import configs
env = "default"
app.config.from_object(configs[env])
