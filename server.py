

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
# Routes


@app.route('/')
def index():
    """Index."""

    return render_template("index.html")


@app.route('/main')
def main_page():
    """Main page, shows search form"""

    return render_template("main.html")


@app.route('/main_results')
def main_results():
    """Show results from main.html search"""

    char_name_input = request.args.get("char_name_input")
    # char_male_input = request.args.get("char_male_input")
    # char_dead_input = request.args.get("char_dead_input")
    # char_house_input = request.args.get("char_house_input")
    # title_name_input = request.args.get("title_name_input")
    # ep_name_input = request.args.get("ep_name_input")
    # ep_season_input = request.args.get("ep_season_input")

    return render_template(
        "main_results.html",
        char_name_input=char_name_input,
        # char_male_input=char_male_input,
        # char_dead_input=char_dead_input,
        # char_house_input=char_house_input,
        # title_name_input=title_name_input,
        # ep_name_input=ep_name_input,
        # ep_season_input=ep_season_input
        )



###########################################
# Helper Functions


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
