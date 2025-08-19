import pymongo
import sys
import chess.pgn
import chess

MONGO_CON_STRING = "mongodb://localhost:27017/"
APP_DB_NAME = "chesshpy"

def getGamesFromFile(pgnFile):
    """Get a list of games from an opened pgn file

    Args:
        pgnFile (file): The opened text file containing one or more pgn games

    Returns:
        list[chess.pgn.Game]
    """
    games = []
    while True:
        game = chess.pgn.read_game(pgnFile)
        if game is not None:
            games.append(game)
        else: 
            break
    return games

def convertGameToMongoDoc(game):
    """Converts a game to notation used with the mongo database

    Args:
        game (chess.pgn.Game): input game
    Returns:
        dict: dictionary representing mongo document
    """
    gameDoc = {}
    gameDoc["header"] = dict(game.headers)
    gtmList = []
    #Guess The Move
    board = game.board()

    prevMoveDoc = None
    for nextMove in game.mainline_moves():
        fen = board.fen()
        
        nextMoveDoc = {
           "from" : chess.SQUARE_NAMES[nextMove.from_square], 
            "to" : chess.SQUARE_NAMES[nextMove.to_square], 
            "san" : board.san(nextMove)
        }


        gtmList.append({"fen":fen,"nextMove":nextMoveDoc,"prevMove":prevMoveDoc})
        board.push(nextMove)
        prevMoveDoc = nextMoveDoc

    gameDoc["positions"] = gtmList

    return gameDoc

def uploadToMongo(gameDocs, dbName, collectionName):
    """Uploads a list of pre-processed games to mongo

    Args:
        gameDocs (list[dict]): a list of dictionaries representing games
        dbName (str): database name
        collectionName(str): collection name
    """
    client = pymongo.MongoClient(MONGO_CON_STRING)

    db = client[dbName]

    col = db[collectionName]

    col.insert_many(gameDocs)

def convertPgnsToCollection(pgnFilePath, collectionName):
    """Convert a pgn file to a mongo game collections

    Args:
        pgnFile (str): A path to a pgn file
        collectionName (str): what do we call this collection of games
    """
    pgnFile = open(pgnFilePath,"r")
    games = getGamesFromFile(pgnFile)
    gameDocs = map(convertGameToMongoDoc, games)

    uploadToMongo(gameDocs, APP_DB_NAME, collectionName)


def main():
    if len(sys.argv) != 3:
        print ("Usage: ")
        print("python3 uploadChess.py <filename.pgn> <collectionName>")
        return (1)

    filename = sys.argv[1]
    if not filename.endswith(".pgn"):
        print ("WARNING: file does not end with .pgn")
        print("Uploading anyway...")
    
    convertPgnsToCollection(filename, sys.argv[2])


if __name__ == "__main__":
    main()