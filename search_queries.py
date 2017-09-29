from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from model import connect_to_db, Character, Title, Episode, CharTitle, CharEp

###########################################
# Search Functions


def search_by_id(char_id):
    """Searches by char_id int, pulls all associated info into a dictionary.

        >>> search_by_id()


    """

    char_obj = Character.query.filter(Character.char_id == char_id).first()

    # Basic character info:

    char_id = char_obj.char_id
    char_name = char_obj.char_name
    char_male = char_obj.char_male
    char_house = char_obj.char_house
    char_dead = char_obj.char_dead

    # Title list:

    title_list_obj = CharTitle.query.filter(CharTitle.char_id == char_id).all()

    char_titles = []

    for title in title_list_obj:
        title_num = title.title_id
        title = Title.query.filter(Title.title_id == title_num).first()
        char_titles.append(title.title_name)

    # Episode list:

    ep_list_obj = CharEp.query.filter(CharEp.char_id == char_id).all()

    char_eps = []

    for ep in ep_list_obj:
        ep_num = ep.ep_id
        ep = Episode.query.filter(Episode.ep_id == ep_num).first()
        char_eps.append(ep.ep_name)

    # Populate info dictionary:

    char_info = {}

    char_info['char_id'] = char_id
    char_info['char_name'] = char_name
    char_info['char_male'] = char_male
    char_info['char_dead'] = char_dead
    char_info['char_house'] = char_house
    char_info['char_titles'] = char_titles
    char_info['char_eps'] = char_eps

    return char_info


def search_by_name(name):
    """ Searches by char_name str, returns char_id int.

    """

    char_obj = Character.query.filter(Character.char_name == name).first()

    return char_obj.char_id


def search_by_gender(gender):
    """Searches by char_male (Bool), returns char_ids int list.

    """

    char_obj_list = Character.query.filter(Character.char_male == gender).all()
    char_id_list = []

    for char in char_obj_list:
        char_id_list.append(char.char_id)

    return char_id_list


def search_by_dead(dead):
    """Searches by char_dead str ('Totally', 'Not yet', 'Unknown', returns char_ids int list.

    """

    char_obj_list = Character.query.filter(Character.char_dead == dead).all()
    char_id_list = []

    for char in char_obj_list:
        char_id_list.append(char.char_id)

    return char_id_list


def search_by_house(house):
    """Searches by char_house str, returns char_ids int list.

    """

    char_obj_list = Character.query.filter(Character.char_house == house).all()
    char_id_list = []

    for char in char_obj_list:
        char_id_list.append(char.char_id)

    return char_id_list


def search_by_title(title):
    """Searches by title_name str, returns char_ids int list.

    """

    title_obj = Title.query.filter(Title.title_name == title).first()

    chartitle_obj_list = CharTitle.query.filter(CharTitle.title_id == title_obj.title_id).all()

    char_id_list = []

    for obj in chartitle_obj_list:
        char_id_list.append(obj.char_id)

    return char_id_list


def search_by_episode(episode):
    """Searches by ep_name str, returns char_ids int list.

    """

    ep_obj = Episode.query.filter(Episode.ep_name == episode).first()

    charep_obj_list = CharEp.query.filter(CharEp.ep_id == ep_obj.ep_id).all()

    char_id_list = []

    for obj in charep_obj_list:
        char_id_list.append(obj.char_id)

    return char_id_list


def search_by_season(season):
    """Searches by ep_season int, returns ep_name str list.

    """

    ep_obj_list = Episode.query.filter(Episode.ep_season == season).all()

    ep_name_list = []

    for ep in ep_obj_list:
        ep_name_list.append(ep.ep_name)

    return ep_name_list


##########################################
# Helper Functions


if __name__ == "__main__":

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


###########################################
# Doc Tests

# if __name__ == "__main__":
#     print
#     import doctest
#     if doctest.testmod().failed == 0:
#         print "*** PASSED! (woot) ***"
#     print
