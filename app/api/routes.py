from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Whiskey, whiskey_schema, whiskeys_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/whiskeys', methods = ['POST'])
@token_required
def create_whiskey(current_user_token):
    distiller = request.json['distiller']
    variety = request.json['variety']
    year = request.json['year']
    tating_notes = request.json['tasting_notes']
    user_token = current_user_token.token

    whiskey = Whiskey(distiller, variety, year, tating_notes, user_token=user_token)

    db.session.add(whiskey)
    db.session.commit()

    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskeys', methods = ['GET'])
@token_required
def get_whiskeys(current_user_token):
    a_user = current_user_token.token
    whiskeys = Whiskey.query.filter_by(user_token = a_user).all()
    response = whiskeys_schema.dump(whiskeys)
    return jsonify(response)

@api.route('/whiskeys/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    car = Whiskey.query.get(id)
    response = whiskey_schema.dump(car)
    return jsonify(response)

@api.route('/whiskeys/<id>', methods = ['POST','PUT'])
@token_required
def update_whiskey(current_user_token,id):
    whiskey = Whiskey.query.get(id) 
    whiskey.distiller = request.json['distiller']
    whiskey.variety = request.json['variety']
    whiskey.year = request.json['year']
    whiskey.tasting_notes = request.json['tasting_notes']
    whiskey.user_token = current_user_token.token

    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskeys/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)