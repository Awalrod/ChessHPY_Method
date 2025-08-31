from flask import Flask, render_template
from chessdb import getChess

app = Flask(__name__)

@app.route("/")
def hello_world():
    chennaiJson = getChess.getAllGamesFromCollection("chennaiTest")
    return render_template('main.html',allGames=chennaiJson)


if __name__ == "__main__":
    app.run(port=5000)