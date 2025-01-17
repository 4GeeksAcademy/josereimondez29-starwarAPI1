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
from models import db, User, Planet, Character, Vehicle_Starship, FavoriteCharacter, FavoritePlanet, FavoriteVehicleStarship
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
    new_user = User(name=data['name'], email=data['email'], password=data['password'], is_active=data['is_active'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify("User successfully added"), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            "id": user.id,
            "username": user.name,
            "email": user.email,
        }
        return jsonify({"message": "User founded", "user": user_data}), 200
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
        planet_data = {
            "id": planet.id,
            "name": planet.name,
            "climate": planet.climate,
            "population": planet.population,
        }
        return jsonify({"message": "Planet found", "planet": planet_data}), 200
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
        character_data = {
            "id": character.id,
            "name": character.name,
            "species": character.species,
            "gender": character.gender,
        }
        return jsonify({"message": "Character found", "character": character_data}), 200
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

@app.route('/user/favorites', methods=['GET'])
def favorites_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': "debes enviar informacion en el body"}), 400
    if 'user_id' not in body:
        return jsonify({'msg': 'El campo user_id es obligatorio'}), 400
    user = User.query.get(body['user_id'])
    if user is None:
        return jsonify({'msg': "El usuario con el id {} no existe".format(body['user_id'])}), 404
    favorite_planets = db.session.query(FavoritePlanet, Planet).join(Planet).filter(FavoritePlanet.user_id==body['user_id']).all()
    favorite_planets_serialized = []
    for favorite_item, planet_item in favorite_planets:
        favorite_planets_serialized.append({"favorite_planet_id": favorite_item.id, "planet": planet_item.serialize()})
        return jsonify({"msg": "ok", "results": favorite_planets_serialized})
    favorite_character= db.session.query(FavoriteCharacter, Character).join(Character).filter(FavoriteCharacter.user_id==body['user_id']).all()
    favorite_character_serialized = []
    for favorite_item, character_item in favorite_character:
        favorite_character_serialized.append({"favorite_character_id": favorite_item.id, "character": character_item.serialize()})
        return jsonify({"msg": "ok", "results": favorite_character_serialized})
    favorite_vehicle_starship= db.session.query(FavoriteVehicleStarship, Vehicle_Starship).join(Vehicle_Starship).filter(FavoriteVehicleStarship.user_id==body['user_id']).all()
    favorite_vehicle_starship_serialized = []
    for favorite_item, vehicle_starship_item in favorite_vehicle_starship:
        favorite_vehicle_starship_serialized.append({"favorite_vehicle_starship_id": favorite_item.id, "starship": vehicle_starship_item.serialize()})
        return jsonify({"msg": "ok", "results": favorite_vehicle_starship_serialized})
    print(user)
    return jsonify({'msg': 'ok'})

    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
