from flask import Flask
from flask_restful import Api

from db import db
# import os
from flask_cors import CORS
from resources.contact import Contact, ContactsList

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)

CORS(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Contact, '/contact')
api.add_resource(ContactsList, '/contacts')


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True, port=5000, host="0.0.0.0")
