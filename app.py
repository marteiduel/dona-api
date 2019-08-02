from flask import Flask, jsonify, request 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os 

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Dona(db.Model):
    __tablename__= "dona"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    image = db.Column(db.String(250))
    price = db.Column(db.Float(10))
    type = db.Column(db.String(15))
    description = db.Column(db.String(70))

    def __init__(self, name, image, price, type, description):
        self.name = name
        self.image = image 
        self.price = price 
        self.type = type
        self.description = description

class DonaSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "type","description")

dona_schema = DonaSchema()
donas_schema = DonaSchema(many=True)


@app.route("/donas", methods=["GET"])
def get_donas():
    all_donas = Dona.query.all()
    result = donas_schema.dump(all_donas)

    return jsonify(result.data)

@app.route("/add-dona", methods=["POST"])
def add_dona():
    name = request.json["name"]
    image = request.json["image"]
    price = request.json["price"]
    type = request.json["type"]
    description = request.json["description"]

    record = Dona(name, image, price, type, description)
    db.session.add(record)
    db.session.commit()

    dona = Dona.query.get(record.id)
    return dona_schema.jsonify(dona)

@app.route("/dona/<id>", methods=["PUT"])
def update_dona(id):
    dona = Dona.query.get(id)

    name = request.json["name"]
    image = request.json["image"]
    price = request.json["price"]
    type = request.json["type"]
    description = request.json["description"]

    dona.name = name

    db.session.commit()
    return jsonify("Updated dona")

@app.route("/dona/<id>", methods=["DELETE"])
def delete_dona(id):
    record = Dona.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("We'll miss you dona!")



if __name__ == "__main__":
    app.debug = True
    app.run()