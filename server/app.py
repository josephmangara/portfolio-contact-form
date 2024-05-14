#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Client

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):
    def get(self):
        return jsonify({"message": "Welcome to the Plants API"})



if __name__ == "__main__":
    app.run(port=4000, debug=True)