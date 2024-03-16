from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    favorites = db.relationship("Favorite", back_populates="user")

    def __repr__(self):
        return f"Usuario con id {self.id} y email: {self.email}"

    def serialize(self):
        return {
            "id": self.id,
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
    

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    user = db.relationship("User", back_populates="favorites")
    planet = db.relationship("Planet")
    character = db.relationship("Character")

   