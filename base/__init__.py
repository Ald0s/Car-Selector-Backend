import atexit
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)

print("> Loading in configuration ...")
app.config.from_object(Config)

print("> Creating database ...")
db = SQLAlchemy(app)

from base.models import Car, Bike, Make
db.create_all()

print("> Importing vehicle set")
Car.Import( "cars.json" )
Bike.Import( "bikes.json" )

db.session.commit()

print("> Importing routes")
from base import routes

print("> Done! Ready to start !")