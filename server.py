

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, Character, Title, Episode, House, CharTitle, CharEp, CharHouse

from search_queries import char_search_by_multiple_args, char_search_by_id
from search_queries import char_search_by_house
from search_queries import ep_search_by_id, title_search_by_id

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

# Look up syntax Params in args.get

    multi_arg_dict['char_name'] = request.args.get("char_name")
    multi_arg_dict["char_male"] = request.args.get("char_male")
    multi_arg_dict["char_dead"] = request.args.get("char_dead")



    list_of_chars = char_search_by_multiple_args(multi_arg_dict)

    for char in list_of_chars:
        if len(list_of_chars) == 1:
            return redirect("/chars/%d" % (char.char_id))
        else:
            return render_template('results.html', list_of_chars=list_of_chars)

##################################################
# Char Routes


@app.route("/chars")
def char_list():
    """Show list of characters."""

    char_list = Character.query.order_by('char_name').all()

    return render_template("char_list.html", char_list=char_list)


@app.route("/chars/<int:char_id>")
def char_details(char_id):
    """Shows char details"""

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
def ep_details(ep_id):
    """Shows episode details"""

    ep_info = ep_search_by_id(ep_id)

    return render_template("ep.html",
                           ep_id=ep_info['ep_id'],
                           ep_name=ep_info['ep_name'],
                           ep_season=ep_info['ep_season'],
                           char_list=ep_info['char_list'])

###########################################
# Title routes


@app.route("/titles")
def title_list():
    """Show list of titles."""

    title_list = Title.query.order_by('title_name').all()

    return render_template("title_list.html", title_list=title_list)


@app.route("/titles/<int:title_id>")
def title_details(title_id):
    """Shows title details"""

    chars_with_title = title_search_by_id(title_id)

    title_obj = Title.query.filter(Title.title_id == title_id).first()
    title_name = title_obj.title_name

    return render_template("title.html",
                           title_id=title_id,
                           title_name=title_name,
                           chars_with_title=chars_with_title)

###########################################
# House routes


# @app.route("/houses")
# def house_list():
#     """Show list of houses."""

# #     query = session.query(Class.title.distinct().label("title"))
# # titles = [row.title for row in query.all()]

#     house_list = db.session.query(Character.char_house.distinct())

#     return render_template("house_list.html", house_list=house_list)


# @app.route("/houses/<int:house_name>")
# def house_details(char_house):
#     """Shows house details"""

#     char_house_list = char_search_by_house(char_house)

#     return render_template("house.html",
#                            char_house=char_house,
#                            char_house_list=char_house_list)

###########################################
# Helper functions


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
