import pymongo
import sys
import chess.pgn
import chess
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# mydb = myclient["mydatabase"]

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

def main():
    if len(sys.argv) != 3:
        print ("Usage: ")
        print("python3 uploadChess.py <filename.pgn> <databasename>")
        return (1)

    filename = sys.argv[1]
    if not filename.endswith(".pgn"):
        print ("WARNING: file does not end with .pgn")
        print("Uploading anyway...")
    
    pgnFile = open(filename,'r')
    games = getGamesFromFile(pgnFile)


if __name__ == "__main__":
    main()