from flask import (
    Flask, render_template, session,
    redirect, url_for, request,
    jsonify
)

from flask_session import Session
from tempfile import mkdtemp

# export FLASK_APP=application

#
# create a flask app from this script
app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def game_turn():
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

@app.route("/")
def index():

    """ Index html scrpt to an html page"""

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    return render_template("tictactoe.html", game = session["board"], turn = session["turn"])



# update the board
# change the whos turn
# redirect the page, restart
@app.route("/play/<int:row>/<int:col>", methods=['GET', 'POST'])
def play(row, col):

    # add move
    session['board'][row][col] = session["turn"]

    # check winner here

    # switch turn
    game_turn()

    return redirect(url_for("index"))

@app.route("/AI")
def withAI():
    pass

@app.route("/reset")
def reset():
    try:
        del(session["board"])
    except KeyError:
        pass
    return redirect(url_for("index"))


