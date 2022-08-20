from boggle import Boggle
from flask import Flask, session, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'B3h3LtWO'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def home_page():

    if 'game_board' in session:
        board = session['game_board']
    else:
        game = Boggle()
        board = game.make_board()
        session['game_board'] = board

    return render_template('boggle.html', board=board)