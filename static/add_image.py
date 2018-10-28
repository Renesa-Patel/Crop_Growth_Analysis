import uuid
from commom.database import Database


class Add_image(object):
    def __init__(self, image_path, s_api_key, s_analyze_flag=False, _id=None):
        self.image_path = image_path
        self.s_api_key = s_api_key
        self.s_analyze_flag = s_analyze_flag
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_api_key(cls, s_api_key):
        data = Database.find_one(collection='data_entries', query={'s_api_key': s_api_key})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(collection='data_entries', query={'_id': _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def add_image(cls, image_path, s_api_key):
        new_image = cls(image_path, s_api_key)
        new_image.save_to_mongo()

    def save_to_mongo(self):
        Database.insert("data_entries", self.json())

    def json(self):
        return {
            "image_path": self.image_path,
            "s_api_key": self.s_api_key,
            "s_analyze_flag": self.s_analyze_flag,
            "_id": self._id
        }
