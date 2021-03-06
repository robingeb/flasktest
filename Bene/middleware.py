import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
from hb_weclapp import *

def main():
    mongo_url = "mongodb+srv://user2:PJS2021@cluster0.hin53.mongodb.net/test"
    client = MongoClient(mongo_url)

    # get configuration decitions of user saved in MongoDB
    erp, update_time = get_config(client)

def get_config(client_mongo):
    db = client_mongo['Keys']
    # TODO: Wo steht welches ERP System ausgewählt wurde?
    col_weclapp = db['Key_Weclapp']
    col_dynamics = db["Key_Dynamics"]
    col_xentral = db["Key_Xentral"]
    col_myfactory = db["Key_MyFactory"]

    if col_myfactory.find():
        print("myfactory:")
        for doc in col_myfactory.find():            
            print(doc)
    # if col_weclapp.find() not None:
    #     print("weclapp")
    #     for doc in col_weclapp.find():
    #         print(doc)
    else:
        print("Error")    
    return 0, 0
    

if __name__ == "__main__":
    main()
    
    

