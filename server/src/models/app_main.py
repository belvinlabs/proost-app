from json import loads
from sqlalchemy.orm import relationship

from models.base import Base, db

from utils.app import dump_json
from utils.database import get_db_url


class User(Base):
    is_authenticated = True
    is_active = True
    is_anonymous = False

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    sub = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False, unique=True)
    given_name = db.Column(db.String(128))
    family_name = db.Column(db.String(128))
    name = db.Column(db.String(128))
    picture_url = db.Column(db.String(500))
    google_credentials = db.Column(db.LargeBinary)
    databases = relationship("UserDatabase", back_populates="user")
    metabase = relationship("UserMetabase", back_populates="user")

    def get_id(self):
        return self.id


class UserDatabase(Base):
    __tablename__ = 'user_databases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    drivername = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    host = db.Column(db.String(256))
    port = db.Column(db.Integer)
    database = db.Column(db.String(128))
    query = db.Column(db.String(256))
    user = relationship("User", back_populates="databases")

    def get_url(self):
        data = dump_json(self)
        return get_db_url(loads(data))


class Settings(Base):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    synced_calendars = db.Column(db.JSON)


class UserMetabase(Base):
    __tablename__ = 'user_metabase'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    user = relationship("User", back_populates="metabase")
