

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, Character, Title, Episode, CharTitle, CharEp

from search_queries import char_search_by_name, char_search_by_gender
from search_queries import char_search_by_dead, char_search_by_house
from search_queries import char_search_by_title, char_search_by_episode
from search_queries import char_search_by_season, char_search_by_id
from search_queries import ep_search_by_id, ep_search_by_season

app = Flask(__name__)

app.secret_key = "SEEKRIT"

app.jinja_env.undefined = StrictUndefined

###########################################
# Main routes


@app.route('/')
def index():
    """Index."""

    return render_template("index.html")


@app.route('/main')
def main_page():
    """Main page, shows search form"""

    return render_template("main.html")


@app.route('/search.html')
def main_search():
    """gets info to use in search"""

    char_name_input = request.args.get("char_name_input")
    char_male_input = request.args.get("char_male_input")
    char_dead_input = request.args.get("char_dead_input")
    char_house_input = request.args.get("char_house_input")
    title_name_input = request.args.get("title_name_input")
    ep_name_input = request.args.get("ep_name_input")
    ep_season_input = request.args.get("ep_season_input")

    char_id = char_search_by_name(char_name_input)


##################################################
# Char Routes


@app.route("/chars")
def char_list():
    """Show list of characters."""

    char_list = Character.query.order_by('char_name').all()
    return render_template("char_list.html", char_list=char_list)


@app.route("/char/<int:char_id>")
def char_info(char_id):
    """Shows char info"""

    char_info = char_search_by_id(char_id)

    char_name = char_info['char_name']
    char_male = char_info['char_male']
    char_dead = char_info['char_dead']
    char_house = char_info['char_house']
    char_titles = char_info['char_titles']
    char_eps = char_info['char_eps']

    return render_template("char.html",
                           char_name=char_name,
                           char_id=char_id,
                           char_male=char_male,
                           char_dead=char_dead,
                           char_house=char_house,
                           char_titles=char_titles,
                           char_eps=char_eps)


##################################################
# Episode routes


@app.route("/eps")
def ep_list():
    """Show list of episodes."""

    ep_list = Episode.query.order_by('ep_season').all()

    return render_template("ep_list.html", ep_list=ep_list)


@app.route("/eps/<int:ep_id>")
def ep_info(ep_id):
    """Shows episode info"""

    # ep_id = request.args.get(ep_id)

    ep_info = ep_search_by_id(ep_id) *****GET********

    return render_template("ep_info.html",
                           ep_id=ep_info.ep_id,
                           ep_name=ep_info.ep_name,
                           ep_season=ep_info.ep_season,
                           char_list=ep_info.char_list)


###########################################
# Title routes


###########################################
# Helper functions


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
