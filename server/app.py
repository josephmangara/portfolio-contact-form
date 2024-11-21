#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Client
from flask_mail import Mail, Message
from flask_cors import CORS

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__,)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


migrate = Migrate(app, db)
mail = Mail(app)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return jsonify({"message": "Clients API"})

api.add_resource(Home, '/')

@app.route("/contact", methods=['POST'])
def send_email():
    try:
        data = request.get_json()

        # Saving client info
        new_client = Client(name=data['name'], email=data['email'], message=data['message'])
        db.session.add(new_client)
        db.session.commit()

        # Sending email
        msg = Message(
            subject=f"Portfolio contact form submission from {data['name']}",
            sender=data['email'],
            recipients=[app.config['MAIL_USERNAME']],   
            body=data['message']
        )
        mail.send(msg)

        return jsonify({"message": "Email sent!"}), 200

    except KeyError as e:
        db.session.rollback()  # Rollback if data save failed
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400

    except Exception as e:
        db.session.rollback()  # Rollback if there's any other error
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5555, debug=True)