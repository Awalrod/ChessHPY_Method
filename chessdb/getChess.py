import pymongo
from chessdb.constants import MONGO_CON_STRING, APP_DB_NAME


def getAllGamesFromCollection(colName):
    client = pymongo.MongoClient(MONGO_CON_STRING)
    db = client[APP_DB_NAME]

    col = db[colName]

    return col.find({},{"_id":0}).to_list()
