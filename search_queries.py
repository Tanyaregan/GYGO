from model import db, connect_to_db, Character, Title, Episode, CharTitle
from model import CharEp, House, CharHouse

###########################################
# Char searches


def char_search_by_id(char_id):
    """Searches by char_id int, pulls all associated info into a dictionary.

    >>> result = char_search_by_id(42).items()
    >>> result.sort()
    >>> result #doctest: +NORMALIZE_WHITESPACE
    [('char_dead', u'Unknown'), ('char_eps', []), ('char_house', u'No Affiliation'),
    ('char_id', 42), ('char_male', False), ('char_name', u'Alaric of Eysen'),
    ('char_titles', [])]

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
    char_house = house_obj.house_name

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


def char_search_by_episode(episode):
    """Searches by ep_name str, returns char_ids int list.

        >>> char_search_by_episode('Breaker of Chains')  #doctest: +ELLIPSIS
        [63, 183, 264, 272, 277, 327, 361, ... 1812, 1854]

        >>> char_search_by_episode('The Night Lands')  #doctest: +ELLIPSIS
        [99, 150, 169, 238, 264, 272, 277, ... 1854, 2016]

    """

    ep_obj = Episode.query.filter(Episode.ep_name == episode).first()

    charep_obj_list = CharEp.query.filter(CharEp.ep_id == ep_obj.ep_id).all()

    char_id_list = []

    for obj in charep_obj_list:
        char_id_list.append(obj.char_id)

    return sorted(char_id_list)


def char_search_by_multiple_args(multi_arg_dict):
    """Searches by arg dict passed from search page, returns list of char objects

        >>> char_search_by_multiple_args({'char_dead':'Totally',
        ... 'char_name':'None', 'char_male':'False'})
        ... #doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        [174, 316, 473, 476,... 1668, 1683, 1746, 1755, 1843, 1888, 2011]

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
# Episode searches


def ep_search_by_id(ep_id):
    """Searches for episode by id, returns episode info

        >>> result = ep_search_by_id(32).items()
        >>> result.sort()
        >>> result #doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        [('char_list', [u'Alliser Thorne', u'Barristan Selmy', u'Bran Stark', ...
        u'Tommen Baratheon', u'Tyrion Lannister']),
        ('ep_id', 32), ('ep_name', u'Breaker of Chains'), ('ep_season', 4)]

    """

    ep_obj = Episode.query.filter(Episode.ep_id == ep_id).first()

    char_id_list = char_search_by_episode(ep_obj.ep_name)

    ep_char_name_list = []

    for char_id in char_id_list:
        char_info = char_search_by_id(char_id)
        name = char_info['char_name']
        ep_char_name_list.append(name)

    ep_info = {}

    ep_info['ep_id'] = ep_obj.ep_id
    ep_info['ep_name'] = ep_obj.ep_name
    ep_info['ep_season'] = ep_obj.ep_season
    ep_info['char_list'] = sorted(ep_char_name_list)

    return ep_info


##########################################
# Title searches


def title_search_by_name(title_name):
    """Searches by title_name str, returns char_ids int list.

        >>> title_search_by_name('Lady')
        [24, 65, 70, 93, 112, 160, 233, 415, 633, 1020, 1170, 1261, 1516, 1650, 1667]

        >>> title_search_by_name('King')
        [557, 1674]

    """
    title_obj = Title.query.filter(Title.title_name == title_name).first()

    title_id = title_obj.title_id

    chartitle_obj_list = CharTitle.query.filter(CharTitle.title_id == title_id).all()

    chars_with_title = []

    for obj in chartitle_obj_list:
        char_id = obj.char_id
        chars_with_title.append(char_id)

    return sorted(chars_with_title)


##########################################
# House searches


def char_search_by_house(house_name):
    """Searches by char_house str, returns char_ids int list.

        >>> char_search_by_house('Tarly')
        [455, 1481, 1751]

    """

    house_char_obj = House.query.filter(House.house_name == house_name).first()
    house_id = house_char_obj.house_id

    house_char_list = []

    house_char_objs = CharHouse.query.filter(CharHouse.house_id == house_id).all()

    for char in house_char_objs:
        char_id = char.char_id
        house_char_list.append(char_id)

    return sorted(house_char_list)


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


###########################################
# Unused functions

# def char_search_by_name(name):
#     """ Searches by char_name str, returns char_id int.

#         >>> char_search_by_name('Jon Snow')
#         925

#         >>> char_search_by_name('Hodor')
#         796

#     """

#     char_obj = Character.query.filter(Character.char_name == name).first()

#     return char_obj.char_id


# def ep_search_by_season(season):
#     """Searches for season, returns all episodes in that season

#         >>> ep_search_by_season(2) #doctest: +NORMALIZE_WHITESPACE
#         [u'A Man Without Honor', u'Blackwater', u'Garden of Bones',
#         u'The Ghost of Harrenhal', u'The Night Lands', u'The North Remembers',
#         u'The Old Gods and the New', u'The Prince of Winterfell', u'Valar Morghulis',
#         u'What Is Dead May Never Die']

#     """

#     season_eps = Episode.query.filter(Episode.ep_season == season).all()

#     ep_names = []

#     for ep in season_eps:
#         ep_names.append(ep.ep_name)

#     return sorted(ep_names)
