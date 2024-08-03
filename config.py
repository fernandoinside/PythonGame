from flask import Flask
from flask_pymongo import PyMongo

class Config:
    SECRET_KEY = 'supersecretkey'
    MONGO_URI = "mongodb://localhost:27017/flaskwebapp"

app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)
