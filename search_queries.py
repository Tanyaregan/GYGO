from model import db, connect_to_db, Character, Title, Episode, CharTitle
from model import CharEp, House, CharHouse

###########################################
# Char searches


def char_search_by_id(char_id):
    """Searches by char_id int, pulls all associated info into a dictionary.

    >>> result = char_search_by_id(925)
    >>> result = sorted(result.values())
    >>> result #doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    [True, 925, <house_id=146 house_name=Stark>,
    [<episode_id=1 ep_season=1 ep_name=The Kingsroad>, ...],
    [<title_id=127 title_name=Lord Commander of the Night's Watch>],
    u'Jon Snow', u'Sorta']
    """

    char_obj = Character.query.filter(Character.char_id == char_id).first()

    # Basic character info:

    char_id = char_obj.char_id
    char_name = char_obj.char_name
    char_male = char_obj.char_male
    char_dead = char_obj.char_dead

    # House:

    charhouse_obj = CharHouse.query.filter(CharHouse.char_id == char_id).first()
    house_id = charhouse_obj.house_id

    house_obj = House.query.filter(House.house_id == house_id).first()

    # Title list:

    title_list_obj = CharTitle.query.filter(CharTitle.char_id == char_id).all()

    title_objs = []

    for title in title_list_obj:
        title_num = title.title_id
        title_obj = Title.query.filter(Title.title_id == title_num).first()
        title_objs.append(title_obj)

    # Episode list:

    ep_list_obj = CharEp.query.filter(CharEp.char_id == char_id).all()

    ep_objs = []

    for ep in ep_list_obj:
        ep_num = ep.ep_id
        ep_obj = Episode.query.filter(Episode.ep_id == ep_num).first()
        ep_objs.append(ep_obj)

    # Populate info dictionary:

    char_info = {}

    char_info['char_id'] = char_id
    char_info['char_name'] = char_name
    char_info['char_male'] = char_male
    char_info['char_dead'] = char_dead
    char_info['house_obj'] = house_obj
    char_info['title_objs'] = title_objs
    char_info['ep_objs'] = ep_objs

    return char_info


def char_search_by_multiple_args(multi_arg_dict):
    """Searches by arg dict passed from search page, returns list of char ids

        >>> char_search_by_multiple_args({'char_dead':'Totally',
        ... 'char_name':'None', 'char_male':'False'})
        ... #doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        [174, 316, 473, 476, 526, 836, ... 1353, 1668, 1683, 1843, 2011]

        >>> char_search_by_multiple_args({'char_dead':'Undead'})
        [2029]

        """

    # Makes new dict removing anything that has None/blank

    arg_dict = {}

    for arg, value in multi_arg_dict.items():
        if value == 'None' or not value:
            pass
        else:
            arg_dict[arg] = value

    # Passes list of 1-3 items into query, returns list of char objects

    list_of_chars = Character.query.filter_by(**arg_dict).all()

    list_of_char_ids = []

    for char in list_of_chars:
        list_of_char_ids.append(char.char_id)

    return sorted(list_of_char_ids)


##########################################
# Episode search


def ep_search_by_id(ep_id):
    """Searches for episode by id, returns episode info

        >>> result = ep_search_by_id(32)
        >>> result #doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {...'ep_name': u'Breaker of Chains'...}

    """

    ep_obj = Episode.query.filter(Episode.ep_id == ep_id).first()

    char_id_list = CharEp.query.filter(CharEp.ep_id == ep_id).all()

    ep_char_obj_list = []

    for obj in char_id_list:
        char_id = obj.char_id
        char_obj = Character.query.filter(Character.char_id == char_id).first()
        ep_char_obj_list.append(char_obj)

    ep_info = {}

    ep_info['ep_id'] = ep_obj.ep_id
    ep_info['ep_name'] = ep_obj.ep_name
    ep_info['ep_season'] = ep_obj.ep_season
    ep_info['char_list'] = sorted(ep_char_obj_list)

    return ep_info


##########################################
# Title search


def title_search_by_id(title_id):
    """Searches by title_id int, returns char_ids int list.

    >>> title_search_by_id(197)
    [890]

    """
    title_obj = Title.query.filter(Title.title_id == title_id).first()

    title_id = title_obj.title_id

    chars_with_title = []

    chartitle_obj_list = CharTitle.query.filter(CharTitle.title_id == title_id).all()

    for obj in chartitle_obj_list:
        char_id = obj.char_id
        chars_with_title.append(char_id)

    return sorted(chars_with_title)


##########################################
# House search


def char_search_by_house(house_id):
    """Searches by house_id int, returns ep info and char_ids int list.
    >>> char_search_by_house(42) #doctest: +NORMALIZE_WHITESPACE
    [<char_id=939 name=Jory Cassel male=True dead=Totally>,
    <char_id=1565 name=Rodrik Cassel male=True dead=Totally>]
    """

    house_obj = House.query.filter(House.house_id == house_id).first()

    house_id = house_obj.house_id

    house_char_obj_list = []

    house_char_objs = CharHouse.query.filter(CharHouse.house_id == house_id).all()

    for obj in house_char_objs:
        char_obj = Character.query.filter(Character.char_id == obj.char_id).first()
        house_char_obj_list.append(char_obj)

    return sorted(house_char_obj_list)


##########################################
# Helper Functions


if __name__ == "__main__":

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


###########################################
# Doc Tests

if __name__ == "__main__":
    print
    import doctest
    if doctest.testmod().failed == 0:
        print "*** PASSED! (woot) ***"
    print

