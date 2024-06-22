from app.models.ipersistence_manager import IPersistenceManager
import json
import os

class DataManager(IPersistenceManager):
    def __init__(self, storage_path="data_storage.json"):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump({}, f)

    def save(self, entity):
        with open(self.storage_path, 'r') as f:
            data = json.load(f)
        entity_type = entity.__class__.__name__
        if entity_type not in data:
            data[entity_type] = {}
        data[entity_type][str(entity.id)] = entity.__dict__
        with open(self.storage_path, 'w') as f:
            json.dump(data, f)

    def get(self, entity_id, entity_type):
        with open(self.storage_path, 'r') as f:
            data = json.load(f)
        if entity_type in data and entity_id in data[entity_type]:
            return data[entity_type][entity_id]
        return None

    def update(self, entity):
        self.save(entity)

    def delete(self, entity_id, entity_type):
        with open(self.storage_path, 'r') as f:
            data = json.load(f)
        if entity_type in data and entity_id in data[entity_type]:
            del data[entity_type][entity_id]
        with open(self.storage_path, 'w') as f:
            json.dump(data, f)
