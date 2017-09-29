from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from model import connect_to_db, Character, Title, Episode, CharTitle, CharEp

###########################################
# Search Functions


def search_by_id(char_id):
    """Searches by char_id int, pulls all associated info into a dictionary.

        >>> search_by_id(666)
        {'char_dead': u'Unknown', 'char_eps': [], 'char_house': u'House Morrigen', 'char_id': 666, 'char_male': True, 'char_name': u'Grance Morrigen', 'char_titles': [u'Ser']}

        >>> search_by_id(42)
        {'char_dead': u'Unknown', 'char_eps': [], 'char_house': u'No Affiliation',  'char_id': 42, 'char_male': False, 'char_name': u'Alaric of Eysen', 'char_titles': []}

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

        >>> search_by_name('Jon Snow')
        925

        >>> search_by_name('Hodor')
        796

    """

    char_obj = Character.query.filter(Character.char_name == name).first()

    return char_obj.char_id


def search_by_gender(gender):
    """Searches by char_male (Bool), returns char_ids int list.

        >>> search_by_gender(False) #doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        [23, 33, 36, 38, 42, 43, 47, 51, 53, 57, 65, 66, 68, 70, 72, 80, 81, 82, 84,
        86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, (...)]




    """

    char_obj_list = Character.query.filter(Character.char_male == gender).all()
    char_id_list = []

    for char in char_obj_list:
        char_id_list.append(char.char_id)

    return sorted(char_id_list)


def search_by_dead(dead):
    """Searches by char_dead str ('Totally', 'Not yet', 'Unknown', Undead), 'Sorta'),
       returns char_ids int list.

        >>> search_by_dead('Undead')
        [216, 2035]

        >>> search_by_dead('Sorta')
        [925]

    """

    char_obj_list = Character.query.filter(Character.char_dead == dead).all()
    char_id_list = []

    for char in char_obj_list:
        char_id_list.append(char.char_id)

    return sorted(char_id_list)


def search_by_house(house):
    """Searches by char_house str, returns char_ids int list.

        >>> search_by_house('House Tarly')  #doctest: +NORMALIZE_WHITESPACE
        [455, 1481, 1751]

        >>> search_by_house('Brotherhood without banners')  #doctest: +NORMALIZE_WHITESPACE
        [111, 432, 676, 834, 981, 1010, 1112, 1218, 1258, 1421, 1781, 1802, 1945]

    """

    char_obj_list = Character.query.filter(Character.char_house == house).all()
    char_id_list = []

    for char in char_obj_list:
        char_id_list.append(char.char_id)

    return sorted(char_id_list)


def search_by_title(title):
    """Searches by title_name str, returns char_ids int list.

        >>> search_by_title('Lady') #doctest: +NORMALIZE_WHITESPACE
        [24, 65, 70, 93, 112, 160, 233, 415, 633, 1020, 1170, 1261, 1516, 1650, 1667]

        >>> search_by_title('Protector of the Realm') #doctest: +NORMALIZE_WHITESPACE
        [29, 162, 327, 384, 508, 974, 1906]

    """

    title_obj = Title.query.filter(Title.title_name == title).first()

    chartitle_obj_list = CharTitle.query.filter(CharTitle.title_id == title_obj.title_id).all()

    char_id_list = []

    for obj in chartitle_obj_list:
        char_id_list.append(obj.char_id)

    return sorted(char_id_list)


def search_by_episode(episode):
    """Searches by ep_name str, returns char_ids int list.

        >>> search_by_episode('Breaker of Chains')  #doctest: +NORMALIZE_WHITESPACE
        [63, 183, 264, 272, 277, 327, 361, 372, 388, 463, 500, 678, 680, 795, 796, 850, 852, 925, 937, 1152, 1187, 1231, 1405, 1409, 1425, 1644, 1648, 1812, 1854]

        >>> search_by_episode('The Night Lands')  #doctest: +NORMALIZE_WHITESPACE
        [99, 150, 169, 238, 264, 272, 277, 316, 327, 361, 631, 635, 647, 796, 803, 848, 875, 925, 1041, 1054, 1152, 1288, 1405, 1413, 1508, 1601, 1644, 1648, 1668, 1782, 1790, 1812, 1854, 2016]

    """

    ep_obj = Episode.query.filter(Episode.ep_name == episode).first()

    charep_obj_list = CharEp.query.filter(CharEp.ep_id == ep_obj.ep_id).all()

    char_id_list = []

    for obj in charep_obj_list:
        char_id_list.append(obj.char_id)

    return sorted(char_id_list)


def search_by_season(season):
    """Searches by ep_season int, returns ep_name str list.

        >>> search_by_season(4)  #doctest: +NORMALIZE_WHITESPACE
        [u'Breaker of Chains', u'First of His Name', u'Mockingbird', u'Oathkeeper',
        u'The Children', u'The Laws of Gods and Men', u'The Lion and the Rose',
        u'The Mountain and the Viper', u'The Watchers on the Wall', u'Two Swords']

        >>> search_by_season(2)  #doctest: +NORMALIZE_WHITESPACE
        [u'A Man Without Honor', u'Blackwater', u'Garden of Bones',
        u'The Ghost of Harrenhal',  u'The Night Lands', u'The North Remembers',
        u'The Old Gods and the New', u'The Prince of Winterfell', u'Valar Morghulis',
        u'What Is Dead May Never Die']

    """

    ep_obj_list = Episode.query.filter(Episode.ep_season == season).all()

    ep_name_list = []

    for ep in ep_obj_list:
        ep_name_list.append(ep.ep_name)

    return sorted(ep_name_list)


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
