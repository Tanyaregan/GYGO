

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, Character, Title, Episode, CharTitle, CharEp

from search_queries import char_search_by_multiple_args, char_search_by_id
from search_queries import ep_search_by_id


app = Flask(__name__)

app.secret_key = "SEEKRIT"

app.jinja_env.undefined = StrictUndefined

###########################################
# Main routes


@app.route('/')
def index():
    """Index."""

    return render_template("index.html")


@app.route('/search')
def main_search():
    """gets info to use in search"""

    return render_template('search.html')


@app.route('/results')
def results():
    """Returns a list of chars who fit search criteria"""

    multi_arg_dict = {}

    multi_arg_dict['char_name'] = request.args.get("char_name")
    multi_arg_dict["char_male"] = request.args.get("char_male")
    multi_arg_dict["char_dead"] = request.args.get("char_dead")
    multi_arg_dict["char_house"] = request.args.get("char_house")

    print multi_arg_dict

    list_of_chars = char_search_by_multiple_args(multi_arg_dict)

    return render_template('results.html', list_of_chars=list_of_chars)


##################################################
# Char Routes


@app.route("/chars")
def char_list():
    """Show list of characters."""

    char_list = Character.query.order_by('char_name').all()

    return render_template("char_list.html", char_list=char_list)


@app.route("/chars/<int:char_id>")
def char_info(char_id):
    """Shows char info"""

    char_info = char_search_by_id(char_id)

    return render_template("char.html",
                           char_name=char_info['char_name'],
                           char_id=char_info['char_id'],
                           char_male=char_info['char_male'],
                           char_dead=char_info['char_dead'],
                           char_house=char_info['char_house'],
                           char_titles=char_info['char_titles'],
                           char_eps=char_info['char_eps'])


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

    ep_info = ep_search_by_id(ep_id)

    return render_template("ep.html",
                           ep_id=ep_info['ep_id'],
                           ep_name=ep_info['ep_name'],
                           ep_season=ep_info['ep_season'],
                           char_list=ep_info['char_list'])


###########################################
# House routes


###########################################
# Helper functions


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
