"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = [{
        "family": members
    }]
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    response_body = {
        "member": member
    }
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def create_member():
    
    body = request.get_json()
    if request.content_type == 'application/json':
        if body is None:
            return jsonify({"message": "El body solicitado se encuentra vacio"}), 400
        if "first_name" not in body:
            return jsonify({"message": "Debe especificar first_name"}), 400
        if "age" not in body:
            return jsonify({"message": "Debe especificar age"}), 400
        if "lucky_numbers" not in body:
            return jsonify({"message": "Debe especificar lucky_numbers"}), 400
    else:
        return jsonify({"message": "Error el body debe ser JSON"}), 400
    try:
        member = body
        jackson_family.add_member(member)
        return jsonify({"message": "Se ha agregado un nuevo member con exito"}), 200
    except Exception as error:
        return jsonify({"message": "Ha ocurrido un error inesperado!"}), 500


@app.route('/member/<int:member_id>', methods=['DELETE'])
def remove_member(member_id):
    jackson_family.delete_member(member_id)
    response_body = {
        "done": True
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
