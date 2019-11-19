import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.base import Base, db


class Sync(Base):
    __tablename__ = 'sync'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(256))
    start = db.Column(db.DateTime, comment='A timestamp of when the sync started')
    end = db.Column(db.DateTime, comment='A timestamp of when the sync started')
    message = db.Column(db.Text)
    tasks = relationship("SyncTask", back_populates="sync")
    user = relationship("User")


class SyncTask(Base):
    __tablename__ = 'sync_task'
    id = db.Column(db.Integer, primary_key=True)
    sync_id = db.Column(db.Integer, db.ForeignKey('sync.id'), nullable=False)
    class_name = db.Column(db.String(256))
    commit_id = db.Column(db.String(256), comment='This is a unique ID that represents a database commit. In the case of calendar sync, the commits are done on a cal by cal basis and therefore the commit ID should be the Calendar ID')
    status = db.Column(db.String(256))
    message = db.Column(db.Text)
    errors = db.Column(db.Text)
    pull_start = db.Column(db.DateTime, comment='A timestamp of when pulling data for a commit started')
    pull_end = db.Column(db.DateTime, comment='A timestamp of when pulling data for a commit ended')
    store_start = db.Column(db.DateTime, comment='A timestamp of storing data for a commit started')
    store_end = db.Column(db.DateTime, comment='A timestamp of storing data for a commit ended')
    sync = relationship("Sync", back_populates="tasks")