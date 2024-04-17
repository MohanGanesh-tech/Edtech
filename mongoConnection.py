from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://Ganesh:Mohanganeshn944870@edtech.zinosyp.mongodb.net/?retryWrites=true&w=majority&appName=edtech"

def MongodbConnections():
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)