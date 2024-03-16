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

# Allow CORS requests to this API
api = Blueprint('api', __name__)

CORS(api)

api_blueprint = Blueprint('api', __name__)

# User Routes
@api_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    return jsonify([user.to_dict() for user in users]), 200

@api_blueprint.route('/user', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(email=data['email'], password=data['password'], is_active=data['is_active'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@api_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404

@api_blueprint.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.json
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.is_active = data.get('is_active', user.is_active)
        db.session.commit()
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404

@api_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404

# Planet Routes
@api_blueprint.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.to_dict() for planet in planets]), 200

@api_blueprint.route('/planet', methods=['POST'])
def add_planet():
    data = request.json
    new_planet = Planet(name=data['name'], climate=data['climate'], population=data['population'])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.to_dict()), 201

@api_blueprint.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.to_dict()), 200
    return jsonify({"message": "Planet not found"}), 404

@api_blueprint.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        data = request.json
        planet.name = data.get('name', planet.name)
        planet.climate = data.get('climate', planet.climate)
        planet.population = data.get('population', planet.population)
        db.session.commit()
        return jsonify(planet.to_dict()), 200
    return jsonify({"message": "Planet not found"}), 404

@api_blueprint.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": "Planet deleted"}), 200
    return jsonify({"message": "Planet not found"}), 404

# Character Routes
@api_blueprint.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.to_dict() for character in characters]), 200

@api_blueprint.route('/character', methods=['POST'])
def add_characters():
    data = request.json
    new_character = Character(name=data['name'], species=data['species'], homeworld=data['homeworld'])
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.to_dict()), 201

@api_blueprint.route('/character/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character = Character.query.get(character_id)
    if character:
        data = request.json
        character.name = data.get('name', character.name)
        character.species = data.get('species', character.species)
        character.homeworld = data.get('homeworld', character.homeworld)
        db.session.commit()
        return jsonify(character.to_dict()), 200
    return jsonify({"message": "Character not found"}), 404
@api_blueprint.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if character:
        db.session.delete(character)
        db.session.commit()
        return jsonify({"message": "Character deleted"}), 200
    return jsonify({"message": "Character not found"}), 404

# Favorite Routes
@api_blueprint.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([favorite.to_dict() for favorite in favorites]), 200

@api_blueprint.route('/favorite', methods=['POST'])
def add_favorite():
    data = request.json
    new_favorite = Favorite(user_id=data['user_id'], planet_id=data['planet_id'], character_id=data['character_id'])
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.to_dict()), 201

@api_blueprint.route('/favorite/<int:favorite_id>', methods=['PUT'])
def update_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if favorite:
        data = request.json
        favorite.user_id = data.get('user_id', favorite.user_id)
        favorite.planet_id = data.get('planet_id', favorite.planet_id)
        favorite.character_id = data.get('character_id', favorite.character_id)
        db.session.commit()
        return jsonify(favorite.to_dict()), 200
    return jsonify({"message": "Favorite not found"}), 404

@api_blueprint.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite deleted"}), 200
    return jsonify({"message": "Favorite not found"}), 404

@api_blueprint.route('/hello', methods=['GET'])
def handle_hello():
    return jsonify({"message": "Hello from the backend!"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
