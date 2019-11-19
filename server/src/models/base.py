from flask_sqlalchemy import SQLAlchemy as FlaskSQLAlchemy
from sqlalchemy.sql import func

db = FlaskSQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
