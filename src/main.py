"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Contact
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/contacts', methods=['GET'])
def getAllConctacts():
    contacts_query = Contact.query.all()
    contacts_query = list(map(lambda x: x.serialize(), contacts_query))
    return jsonify(contacts_query), 200



@app.route('/add', methods=['POST'])
def create_Contact():
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'full_name' not in body:
        raise APIException('You need to specify the full_name', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'phone' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'address' not in body:
        raise APIException('You need to specify the email', status_code=400)
    user1 = Contact(full_name=body['full_name'], email=body['email'],address=body["address"],phone=body["phone"])
    db.session.add(user1)
    db.session.commit()
    return "Contact Added Successfully", 200



@app.route('/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    user1 = Contact.query.get(contact_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    if "full_name" in body:
        user1.full_name = body["full_name"]
    if "email" in body:
        user1.email = body["email"]
    if "phone" in body:
        user1.phone = body["phone"]
    if "address" in body:
        user1.address = body["address"]
    db.session.commit()
    return jsonify(user1.serialize()), 200



@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_1_Contact(contact_id):
    user1 = Contact.query.get(contact_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    return jsonify(user1.serialize()), 200



@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_Contact(contact_id):
    user1 = Contact.query.get(contact_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    return jsonify(user1.serialize()), 200


# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
