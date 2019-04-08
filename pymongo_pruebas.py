import pymongo
client = pymongo.MongoClient()
db = client.test
users = db.users
users
smith = {"last_name": "Smith", "age": 30}
jones = {"last_name": "Jones", "age": 40}
users.insert_one(smith)
usuario_encontrado  = users.find_one({"last_name": "Smith"})
print(usuario_encontrado)