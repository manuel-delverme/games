from flask import (
    Flask, render_template, session,
    redirect, url_for, request,
    jsonify
)

from flask_session import Session
from tempfile import mkdtemp
import random
from copy import deepcopy
import functools
from blocks_src import findEmptyCells, minimax, pick_random_move, game_turn, check_winner

# export FLASK_APP=application
# app.run(host="0.0.0.0:PORT#")
# ./ngrok http localhost:PORT#

# create a flask app from this script
app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    """ Index html script to an html page"""

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["winner"] = None

    return render_template("tictactoe.html", game=session["board"], turn=session["turn"], winner=session["winner"])


@app.route("/play/<int:row>/<int:col>", methods=['GET', 'POST'])
def play(row, col):
    """ Update the board, change the whos turn, redirect the page, restart """

    # add move
    session['board'][row][col] = session["turn"]

    # check winner here
    session["winner"] = check_winner(session["board"])

    # switch turn
    session["turn"] = game_turn(session["turn"])

    # TODO: how to stop playing after winning? this does not return winner
    # if session["winner"] != None:
    #     reset()

    return redirect(url_for("index"))


@app.route("/random_player")
def random_player():
    move = pick_random_move(session["board"])
    return redirect(url_for("play", row=move[0], col=move[1]))


@app.route("/withAI")
def with_ai():
    game = [[None, None, None], [None, None, None], [None, None, None]]
    for i in range(3):
        for j in range(3):
            game[i][j] = session["board"][i][j]
    turn = str(session["turn"])
    move = minimax(game, turn)
    return redirect(url_for("play", row=move[1][0], col=move[1][1]))

@app.route("/manu")
def minimax_2():
    game = [[None, None, None], [None, None, None], [None, None, None]]
    for i in range(3):
        for j in range(3):
            game[i][j] = session["board"][i][j]
    actions = findEmptyCells(game)
    turn = str(session["turn"])
    move = minimax(game, actions, turn)
    return redirect(url_for("play", row=move[0][0], col=move[0][1]))

@app.route("/reset")
def reset():
    try:
        del(session["board"])
    except KeyError:
        pass
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0:1111")


