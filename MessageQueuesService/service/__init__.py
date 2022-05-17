from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)  # create Flask application
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///message_queues.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db provides a class called Model that is a declarative base which can be used to declare models
db = SQLAlchemy(app)


from MessageQueuesService.service import message_queues_service

