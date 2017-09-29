

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, Character, Title, Episode, CharTitle, CharEp

from search_queries import search_by_name, search_by_gender, search_by_dead
from search_queries import search_by_house, search_by_title, search_by_episode
from search_queries import search_by_season


app = Flask(__name__)

app.secret_key = "SEEKRIT"

app.jinja_env.undefined = StrictUndefined


###########################################
# Helper Functions


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
