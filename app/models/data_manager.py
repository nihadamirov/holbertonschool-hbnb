from app.models.ipersistence_manager import IPersistenceManager
from app import db  
from datetime import datetime

class DataManager(IPersistenceManager):
    def __init__(self):
        pass  

    def save(self, entity):
        db.session.add(entity)
        db.session.commit()

    def get(self, entity_id, entity_type):
        return db.session.query(entity_type).filter_by(id=entity_id).first()

    def update(self, entity):
        entity.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self, entity_id, entity_type):
        entity = db.session.query(entity_type).filter_by(id=entity_id).first()
        if entity:
            db.session.delete(entity)
            db.session.commit()
