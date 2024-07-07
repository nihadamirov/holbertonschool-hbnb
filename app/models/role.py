from . import db
from .base import BaseModel

class Role(BaseModel):
    __tablename__ = 'roles'
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)