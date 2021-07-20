"""This module defines an customized MongoDB CRUD object.

CRUD
: Connect, Read, Update, Delete

  Typical usage example:

  mydb = MongoCRUD(db_info)
  data = mydb.getCollList()
"""
import pymongo

class MongoCRUD:

    def __init__(self, userId, userPwd, host, port, dbName):
        self.userId = userId
        self.userPwd = userPwd
        self.host = host
        self.port = port
        self.dbName = dbName
        self.db = self.connectDB()

    # Connect
    def connectDB(self):
        self.conn = pymongo.MongoClient("mongodb://"+self.userId+\
            ":"+self.userPwd+"@"+self.host+\
                ":"+self.port+"/"+self.dbName)
        return self.conn.get_database(self.dbName)

    # Switch Database
    def switchDB(self,dbName):
        self.dbName = dbName
        self.db = self.conn.get_database(self.dbName)
    
    # Get current's DB name
    def getDBName(self):
        return self.db
    
    # Read
    def getCollList(self):
        return self.db.list_collection_names()

    def getOneData(self, collection, condition=None):
        return self.db[collection].find_one(condition)

    def getManyData(self, collection, condition=None):
        return self.db[collection].find(condition)

    # Update
    def insertOne(self, collection, data):
        return self.db[collection].insert_one(data)
    
    def insertMany(self, collection, data):
        return self.db[collection].insert_many(data)
    
    def updateOne(self,collection,ori_data,new_data):
        return self.db[collection].update_one(ori_data, new_data)
    
    def updateMany(self,collection,ori_data,new_data):
        return self.db[collection].update_many(ori_data, new_data)

    # Delete
    def deleteOne(self,collection,condition):
        return self.db[collection].delete_one(condition)
    
    def deleteMany(self,collection,condition):
        return self.db[collection].delete_many(condition)


if __name__=="__main__":
    import json

    with open('./meta_manager/config.json', 'r') as f:
        config = json.load(f)
    
    db_info = config['DB_INFO']
    mydb = MongoCRUD(db_info['USER_ID']\
        ,db_info["USER_PWD"],db_info["HOST_ADDR"]\
        ,db_info["HOST_PORT"],db_info["DB_NAME"])
    
    colls = mydb.getCollList()
    print(colls)
    
    collection_name = colls[0]
    
    items = mydb.getManyData(collection_name)
    for item in items:
        print(item)
    