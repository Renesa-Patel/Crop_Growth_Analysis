import pymongo
import pymongo.errors


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    # URI = "mongodb://Admin_RK:Admin@cluster0-shard-00-00-m2mls.mongodb.net:27017,cluster0-shard-00-01-m2mls.mongodb.net:27017,cluster0-shard-00-02-m2mls.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
    DATABASE = None

    @staticmethod
    def initialize():
        try:
            client = pymongo.MongoClient(Database.URI)
            Database.DATABASE = client['Crop_Growth_Analysis']
        except:
            pass

    @staticmethod
    def insert(collection, data):
        data = Database.DATABASE[collection].insert(data)
        return data

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_sort(collection, query, sort_para):
        return Database.DATABASE[collection].find(query).sort(sort_para)

    @staticmethod
    def find_distinct(collection, query, tags):
        return Database.DATABASE[collection].find(query).distinct(tags)

    @staticmethod
    def find_some_rows(collection, query, rows):
        return Database.DATABASE[collection].find(query, rows)

    @staticmethod
    def count_of(collection, query):
        return Database.DATABASE[collection].find(query).count()

    @staticmethod
    def update_one(collection, query, change):
        return Database.DATABASE[collection].update_one(query, change)

    @staticmethod
    def update_many(collection, query, change):
        return Database.DATABASE[collection].update_many(query, change)

    @staticmethod
    def aggregate(collection, query):
        return Database.DATABASE[collection].aggregate(query)

    @staticmethod
    def delete(collection, query):
        return Database.DATABASE[collection].delete_many(query)

    @staticmethod
    def delete_one(collection, query):
        return Database.DATABASE[collection].delete_one(query)