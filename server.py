

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, Character, Title, Episode, House
from model import CharTitle, CharEp, CharHouse

from search_queries import char_search_by_multiple_args, char_search_by_id
from search_queries import char_search_by_house
from search_queries import ep_search_by_id, title_search_by_id

from api_queries import search_term_char_name, wikia_char_article_id, wikia_char_thumb
from api_queries import char_page_etsy, char_page_ebay
from api_queries import item_page_etsy, item_page_ebay

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

    list_of_char_ids = char_search_by_multiple_args(multi_arg_dict)
    list_of_chars = []

    if len(list_of_char_ids) == 0:
        return render_template('not_found.html')

    for char_id in list_of_char_ids:
        char_obj = char_search_by_id(char_id)

        if len(list_of_char_ids) == 1:
            return redirect("/chars/%d" % (char_obj['char_id']))

        else:
            list_of_chars.append(char_obj)

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

    char = char_info['char_name']

    wik_search_name = search_term_char_name(char)
    wik_char_id = wikia_char_article_id(wik_search_name)
    char_thumb = wikia_char_thumb(wik_char_id)

    etsy_items = char_page_etsy(char)

    ebay_items = char_page_ebay(char)

    return render_template("char.html",
                           char_name=char_info['char_name'],
                           char_id=char_info['char_id'],
                           char_male=char_info['char_male'],
                           char_dead=char_info['char_dead'],
                           char_house=char_info['house_obj'],
                           char_titles=char_info['title_objs'],
                           char_eps=char_info['ep_objs'],
                           char_thumb=char_thumb,
                           etsy_items=etsy_items,
                           ebay_items=ebay_items)


@app.route("/chars/<int:char_id>/item")
def char_item_details(char_id):
    """Shows more items for sale relating to char."""

    char_info = char_search_by_id(char_id)

    char = char_info['char_name']

    wik_search_name = search_term_char_name(char)
    wik_char_id = wikia_char_article_id(wik_search_name)
    char_thumb = wikia_char_thumb(wik_char_id)

    more_ebay_items = item_page_ebay(char)

    more_etsy_items = item_page_etsy(char)

    return render_template("item.html",
                           char_id=char_id,
                           char_name=char,
                           char_thumb=char_thumb,
                           more_etsy_items=more_etsy_items,
                           more_ebay_items=more_ebay_items)

@app.route("/chars/<int:char_id>/episodes")
def char_ep_details(char_id):
    """Shows more items for sale relating to char."""

    char_info = char_search_by_id(char_id)

    char = char_info['char_name']

    wik_search_name = search_term_char_name(char)
    wik_char_id = wikia_char_article_id(wik_search_name)
    char_thumb = wikia_char_thumb(wik_char_id)


    return render_template("char_eps.html",
                           char_id=char_id,
                           char_name=char,
                           char_thumb=char_thumb,
                           char_eps=char_info['ep_objs'])



##################################################
# Episode routes


@app.route("/episodes")
def ep_list():
    """Show list of episodes."""

    ep_list = Episode.query.order_by('ep_season').all()

    return render_template("ep_list.html", ep_list=ep_list)


@app.route("/episodes/<int:ep_id>")
def ep_details(ep_id):
    """Shows episode details"""

    ep_info = ep_search_by_id(ep_id)

    return render_template("ep.html",
                           ep_id=ep_info['ep_id'],
                           ep_name=ep_info['ep_name'],
                           ep_season=ep_info['ep_season'],
                           char_list=ep_info['char_list'])


###########################################
# House routes


@app.route("/houses")
def house_list():
    """Show list of houses."""

    house_list = House.query.order_by('house_name').all()

    return render_template("house_list.html", house_list=house_list)


@app.route("/houses/<int:house_id>")
def house_details(house_id):
    """Shows house details"""

    house = House.query.filter(House.house_id == house_id).first()

    house_char_obj_list = char_search_by_house(house_id)

    return render_template("house.html",
                           house_name=house.house_name,
                           house_char_obj_list=house_char_obj_list)


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

    title_obj = Title.query.filter(Title.title_id == title_id).first()
    title_id = title_obj.title_id
    title_name = title_obj.title_name

    char_ids_with_title = title_search_by_id(title_id)

    char_objs_with_title = []

    for char_id in char_ids_with_title:
        char_obj = Character.query.filter(Character.char_id == char_id).first()
        char_objs_with_title.append(char_obj)

    return render_template("title.html",
                           title_id=title_id,
                           title_name=title_name,
                           char_objs_with_title=char_objs_with_title)


###########################################
# Helper functions

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
