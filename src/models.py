from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    

    def __repr__(self):
        return f"ID {self.id}, nombre {self.name} y email: {self.email}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "password": self.password
            
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250))
    population = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Planeta {self.id} de nombre {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet_relationship = db.relationship(Planet) 
    

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    species = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    

    def __repr__(self):
        return f"Character {self.id} de nombre {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character_relationship = db.relationship(Character) 

class Vehicle_Starship(db.Model):
    __tablename__ = 'vehicle_starship'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f"Vehicle {self.id} de nombre {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class FavoriteVehicleStarship(db.Model):
    __tablename__ = 'favorite_vehicles_starships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_starship_id = db.Column(db.Integer, db.ForeignKey('vehicle_starship.id'))
    vehicle_starship_relationship = db.relationship(Vehicle_Starship) 





   