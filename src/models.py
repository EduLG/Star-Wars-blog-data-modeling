from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)

    favorites: Mapped[list['Favorite']] = relationship(
        back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # DO NOT serialize the password, it's a security breach
        }


class Planet(db.Model):  # Singular class name
    __tablename__ = 'planets'  # Plural table name
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    diameter: Mapped[str] = mapped_column(String(50), nullable=True)
    rotation_period: Mapped[str] = mapped_column(String(50), nullable=True)
    gravity: Mapped[str] = mapped_column(String(50), nullable=True)
    population: Mapped[str] = mapped_column(String(50), nullable=True)

    characters: Mapped[list['Character']] = relationship(
        back_populates='homeworld')

    favorite_of: Mapped[list['Favorite']] = relationship(
        back_populates='planet')

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "gravity": self.gravity,
            "population": self.population,
        }


class Character(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    height: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(50), nullable=True)
    gender: Mapped[str] = mapped_column(String(50), nullable=True)

    homeworld_id: Mapped[int] = mapped_column(
        ForeignKey('planets.id'), nullable=True)
    homeworld: Mapped['Planet'] = relationship(back_populates='characters')

    favorite_of: Mapped[list['Favorite']] = relationship(
        back_populates='character')

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }


class Starship(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    pilot_id: Mapped[int] = mapped_column(
        ForeignKey('characters.id'), nullable=True)
    pilot: Mapped['Character'] = relationship('Character')
    cost_in_credits: Mapped[str] = mapped_column(String(50), nullable=True)
    length: Mapped[str] = mapped_column(String(50), nullable=True)
    max_speed: Mapped[str] = mapped_column(String(50), nullable=True)
    crew: Mapped[str] = mapped_column(String(50), nullable=True)

    favorite_of: Mapped[list['Favorite']] = relationship(
        back_populates='starship')

    def __repr__(self):
        return f'<Starship {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "pilot_id": self.pilot_id,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_speed": self.max_speed,
            "crew": self.crew,
        }


class Favorite(db.Model):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planets.id'), nullable=True)
    character_id: Mapped[int] = mapped_column(
        ForeignKey('characters.id'), nullable=True)
    starship_id: Mapped[int] = mapped_column(
        ForeignKey('starships.id'), nullable=True)

    user: Mapped['User'] = relationship(back_populates='favorites')
    planet: Mapped['Planet'] = relationship(back_populates='favorite_of')
    character: Mapped['Character'] = relationship(back_populates='favorite_of')
    starship: Mapped['Starship'] = relationship(back_populates='favorite_of')

    def __repr__(self):
        return f'<Favorite user_id={self.user_id}, planet_id={self.planet_id}, character_id={self.character_id}, starship_id={self.starship_id}>'

    def serialize(self):

        data = {
            "id": self.id,
            "user_id": self.user_id,
            "type": None,
            "item_id": None,
            "item_name": None
        }
        if self.planet:
            data["type"] = "planet"
            data["item_id"] = self.planet_id
            data["item_name"] = self.planet.name
        elif self.character:
            data["type"] = "character"
            data["item_id"] = self.character_id
            data["item_name"] = self.character.name
        elif self.starship:
            data["type"] = "starship"
            data["item_id"] = self.starship_id
            data["item_name"] = self.starship.name
        return data
