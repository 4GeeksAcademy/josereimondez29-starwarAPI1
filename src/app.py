"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# User Routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())

    response_body = {
        "msg": "ok",
        "result": users_serialized
    }

    return jsonify(response_body), 200

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(email=data['email'], password=data['password'], is_active=data['is_active'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify("User successfully added"), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"message": "User found"}), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.json
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.is_active = data.get('is_active', user.is_active)
        db.session.commit()
        return jsonify({"message": "User updated"}), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404

# Planet Routes
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()

    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())

    response_body = {
        "msg": "ok",
        "result": planets_serialized
    }

    return jsonify(response_body), 200

@app.route('/planet', methods=['POST'])
def add_planet():
    data = request.json
    new_planet = Planet(name=data['name'], climate=data['climate'], population=data['population'])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify("Planet successfully added"), 201

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify({"message": "Planet found"}), 200
    return jsonify({"message": "Planet not found"}), 404

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        data = request.json
        planet.name = data.get('name', planet.name)
        planet.climate = data.get('climate', planet.climate)
        planet.population = data.get('population', planet.population)
        db.session.commit()
        return jsonify({"message": "Planet updated"}), 200
    return jsonify({"message": "Planet not found"}), 404

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": "Planet deleted"}), 200
    return jsonify({"message": "Planet not found"}), 404

# Character Routes
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()

    characters_serialized = []
    for character in characters:
        characters_serialized.append(character.serialize())

    response_body = {
        "msg": "ok",
        "result": characters_serialized
    }

    return jsonify(response_body), 200

    
@app.route('/character', methods=['POST'])
def add_characters():
    data = request.json
    new_character = Character(name=data['name'], species=data['species'], homeworld=data['homeworld'])
    db.session.add(new_character)
    db.session.commit()
    return jsonify("Character successfully added"), 201

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character:
        return jsonify({"message": "Character found"}), 200
    return jsonify({"message": "Character not found"}), 404

@app.route('/character/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character = Character.query.get(character_id)
    if character:
        data = request.json
        character.name = data.get('name', character.name)
        character.species = data.get('species', character.species)
        character.homeworld = data.get('homeworld', character.homeworld)
        db.session.commit()
        return jsonify({"message": "Character updated"}), 200
    return jsonify({"message": "Character not found"}), 404

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if character:
        db.session.delete(character)
        db.session.commit()
        return jsonify({"message": "Character deleted"}), 200
    return jsonify({"message": "Character not found"}), 404

# Favorite Routes
@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()

    favorites_serialized = []
    for favorite in favorites:
        favorites_serialized.append(favorite.serialize())

    response_body = {
        "msg": "ok",
        "result": favorites_serialized
    }

    return jsonify(response_body), 200

    
@app.route('/favorite', methods=['POST'])
def add_favorite():
    data = request.json
    new_favorite = Favorite(user_id=data['user_id'], planet_id=data['planet_id'], character_id=data['character_id'])
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify("New favorite successfully added"), 201

@app.route('/favorite/<int:favorite_id>', methods=['GET'])
def get_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if favorite:
        return jsonify({"message": "Favorite found"}), 200
    return jsonify({"message": "Favorite not found"}), 404

@app.route('/favorite/<int:favorite_id>', methods=['PUT'])
def update_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if favorite:
        data = request.json
        favorite.user_id = data.get('user_id', favorite.user_id)
        favorite.planet_id = data.get('planet_id', favorite.planet_id)
        favorite.character_id = data.get('character_id', favorite.character_id)
        db.session.commit()
        return jsonify({"message": "Favorite updated"}), 200
    return jsonify({"message": "Favorite not found"}), 404

@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite deleted"}), 200
    return jsonify({"message": "Favorite not found"}), 404

@app.route('/hello', methods=['GET'])
def handle_hello():
    return jsonify({"message": "Hello from the backend!"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
