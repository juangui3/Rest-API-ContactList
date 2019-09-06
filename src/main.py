"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person
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


@app.route('/person', methods=['POST'])
def post_person():

    # First we get the payload json
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)

    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'address' not in body:
        raise APIException('You need to specify the address', status_code=400)

    # at this point, all data has been validated, we can proceed to inster into the bd
    user1 = Person(full_name=body['full_name'], email=body['email'], address=body['address'], agenda_slug=body['agenda_slug'], phone=body['phone'])
    db.session.add(user1)
    db.session.commit()
    return "ok", 200

@app.route('/person/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    """
    Single person
    """
    if request.method == 'PUT':
        user1 = Person.query.get(person_id)
    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if "full_name" in body:
        user1.full_name = body['full_name']
    if "address" in body:
        user1.address = body['address']
    if "email" in body:
        user1.email = body['email']
    if "phone" in body:
        user1.phone = body['phone']
        user1.agenda_slug = "new_contact_agenda"
        db.session.commit()

        return jsonify(user1.serialize()), 200

    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        return jsonify(user1.serialize()), 200

    return "Invalid Method", 404

@app.route('/person/<int:person_id>', methods=['DELETE'])
def del_single_person(person_id):
    if request.method == 'DELETE':
        user1 = Person.query.get(person_id)

    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    return "ok", 200

@app.route('/contacts', methods=['GET'])
def handle_person():

    people_query = Person.query.all()
    people_query =  list(map(lambda x: x.serialize(), people_query))
    return jsonify(people_query), 200

# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
