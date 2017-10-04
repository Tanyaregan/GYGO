# from flask_sqlalchemy import SQLAlchemy

from model import connect_to_db, Character, Title, Episode, CharTitle, CharEp

###########################################
# Char searches


def char_search_by_id(char_id):
    """Searches by char_id int, pulls all associated info into a dictionary.

        >>> result = char_search_by_id(666).items()
        >>> result.sort()
        >>> result #doctest: +NORMALIZE_WHITESPACE
        [('char_dead', u'Unknown'), ('char_eps', []), ('char_house', u'House Morrigen'),
        ('char_id', 666), ('char_male', True), ('char_name', u'Grance Morrigen'),
        ('char_titles', [u'Ser'])]


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


def char_search_by_name(name):
    """ Searches by char_name str, returns char_id int.

        >>> char_search_by_name('Jon Snow')
        925

        >>> char_search_by_name('Hodor')
        796

    """

    char_obj = Character.query.filter(Character.char_name == name).first()

    return char_obj.char_id


def char_search_by_gender(gender):
    """Searches by char_male (Bool), returns char_ids int list.

        >>> char_search_by_gender(False) #doctest: +ELLIPSIS
        [23, 33, 36, 38, 42, 43, 47, ...]

    """

    char_obj_list = Character.query.filter(Character.char_male == gender).all()
    char_id_list = []

    for char in char_obj_list:
        char_id_list.append(char.char_id)

    return sorted(char_id_list)


def char_search_by_dead(dead):
    """Searches by char_dead str ('Totally', 'Not yet', 'Unknown', 'Undead', 'Sorta'),
       returns char_ids int list.

        >>> char_search_by_dead('Undead')
        [216, 2035]

        >>> char_search_by_dead('Sorta')
        [925]

    """

    char_obj_list = Character.query.filter(Character.char_dead == dead).all()
    char_id_list = []

    for char in char_obj_list:
        char_id_list.append(char.char_id)

    return sorted(char_id_list)


def char_search_by_house(house):
    """Searches by char_house str, returns char_ids int list.

        >>> char_search_by_house('House Tarly')
        [455, 1481, 1751]

        >>> char_search_by_house('Brotherhood without banners')
        [111, 432, 676, 834, 981, 1010, 1112, 1218, 1258, 1421, 1781, 1802, 1945]

    """

    char_obj_list = Character.query.filter(Character.char_house == house).all()
    char_id_list = []

    for char in char_obj_list:
        char_id_list.append(char.char_id)

    return sorted(char_id_list)


def char_search_by_title(title):
    """Searches by title_name str, returns char_ids int list.

        >>> char_search_by_title('Lady')
        [24, 65, 70, 93, 112, 160, 233, 415, 633, 1020, 1170, 1261, 1516, 1650, 1667]

        >>> char_search_by_title('Protector of the Realm')
        [29, 162, 327, 384, 508, 974, 1906]

    """

    title_obj = Title.query.filter(Title.title_name == title).first()

    chartitle_obj_list = CharTitle.query.filter(CharTitle.title_id == title_obj.title_id).all()

    char_id_list = []

    for obj in chartitle_obj_list:
        char_id_list.append(obj.char_id)

    return sorted(char_id_list)


def char_search_by_episode(episode):
    """Searches by ep_name str, returns char_ids int list.

        >>> char_search_by_episode('Breaker of Chains')  #doctest: +NORMALIZE_WHITESPACE
        [63, 183, 264, 272, 277, 327, 361, 372, 388, 463, 500, 678, 680, 795,
        796, 850, 852, 925, 937, 1152, 1187, 1231, 1405, 1409, 1425, 1644,
        1648, 1812, 1854]

        >>> char_search_by_episode('The Night Lands')  #doctest: +NORMALIZE_WHITESPACE
        [99, 150, 169, 238, 264, 272, 277, 316, 327, 361, 631, 635, 647, 796,
        803, 848, 875, 925, 1041, 1054, 1152, 1288, 1405, 1413, 1508, 1601, 1644,
        1648, 1668, 1782, 1790, 1812, 1854, 2016]

    """

    ep_obj = Episode.query.filter(Episode.ep_name == episode).first()

    charep_obj_list = CharEp.query.filter(CharEp.ep_id == ep_obj.ep_id).all()

    char_id_list = []

    for obj in charep_obj_list:
        char_id_list.append(obj.char_id)

    return sorted(char_id_list)


def char_search_by_season(season):
    """Searches by ep_season int, returns ep_name str list.

        >>> char_search_by_season(4)  #doctest: +NORMALIZE_WHITESPACE
        [u'Breaker of Chains', u'First of His Name', u'Mockingbird', u'Oathkeeper',
        u'The Children', u'The Laws of Gods and Men', u'The Lion and the Rose',
        u'The Mountain and the Viper', u'The Watchers on the Wall', u'Two Swords']

        >>> char_search_by_season(2)  #doctest: +NORMALIZE_WHITESPACE
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


def char_search_by_multiple_args(multi_arg_dict):
    """Searches by arg dict passed from search page, returns list of char objects

        >>> char_search_by_multiple_args({'char_dead':'None', 'char_name':'None','char_house':'House Martell', 'char_male':'False'}) #doctest: +NORMALIZE_WHITESPACE
        [<char_id=1052 name=Loreza Sand male=False house=House Martell dead=Totally>,
         <char_id=1320 name=Obara Sand male=False house=House Martell dead=Totally>,
         <char_id=128 name=Arianne Martell male=False house=House Martell dead=Totally>,
         <char_id=1137 name=Manfrey Martell male=False house=House Martell dead=Totally>,
         <char_id=1249 name=Morra male=False house=House Martell dead=Totally>,
         <char_id=1252 name=Mors Martell male=False house=House Martell dead=Totally>,
         <char_id=186 name=Belandra male=False house=House Martell dead=Totally>,
         <char_id=309 name=Cedra male=False house=House Martell dead=Totally>,
         <char_id=476 name=Dorea Sand male=False house=House Martell dead=Totally>,
         <char_id=528 name=Elia Martell male=False house=House Martell dead=Totally>,
         <char_id=525 name=Elia Sand male=False house=House Martell dead=Totally>,
         <char_id=620 name=Gascoyne male=False house=House Martell dead=Totally>,
         <char_id=1202 name=Mellei male=False house=House Martell dead=Totally>,
         <char_id=1314 name=Nymeria male=False house=House Martell dead=Totally>,
         <char_id=1318 name=Nymeria Sand male=False house=House Martell dead=Totally>,
         <char_id=1319 name=Obella Sand male=False house=House Martell dead=Totally>,
         <char_id=1527 name=Ricasso male=False house=House Martell dead=Totally>,
         <char_id=1646 name=Sarella Sand male=False house=House Martell dead=Totally>,
         <char_id=1843 name=Tyene Sand male=False house=House Martell dead=Totally>]

        >>> char_search_by_multiple_args({'char_dead':'Undead'}) #doctest: +NORMALIZE_WHITESPACE
        [<char_id=2035 name=Viserion (Dragon) male=True house=House Targaryen dead=Undead>,
        <char_id=216 name=Benjen Stark male=True house=House Stark dead=Undead>]
    """

    # Makes new dict removing anything that has None

    arg_dict = {}

    for arg, value in multi_arg_dict.items():
        if value == 'None' or not value:
            pass
        else:
            arg_dict[arg] = value

    # Passes list of 1-4 items into query, returns list of char objects

    list_of_chars = Character.query.filter_by(**arg_dict).all()

    return sorted(list_of_chars)

# multi_arg_dict = {'char_house':'House Martell'}


##########################################
# Episode searches


def ep_search_by_id(ep_id):
    """Searches for episode by id, returns episode info

        >>> result = ep_search_by_id(32).items()
        >>> result.sort()
        >>> result #doctest: +NORMALIZE_WHITESPACE
        [('char_list', [u'Alliser Thorne', u'Barristan Selmy', u'Bran Stark',
        u'Brienne of Tarth', u'Bronn', u'Cersei Lannister', u'Craster',
        u'Daario Naharis', u'Daenerys Targaryen', u'Donnel Locke',
        u'Eddison Tollett', u'Grenn', u'Grey Worm', u'Hodor', u'Holly',
        u'Jaime Lannister', u'Janos Slynt', u'Jon Snow', u'Jorah Mormont',
        u'Margaery Tyrell', u'Meera Reed', u'Missandei', u'Petyr Baelish',
        u'Podrick Payne', u'Pypar', u'Samwell Tarly', u'Sansa Stark',
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


def ep_search_by_season(season):
    """Searches for season, returns all episodes in that season

        >>> ep_search_by_season(2) #doctest: +NORMALIZE_WHITESPACE
        [u'A Man Without Honor', u'Blackwater', u'Garden of Bones',
        u'The Ghost of Harrenhal', u'The Night Lands', u'The North Remembers',
        u'The Old Gods and the New', u'The Prince of Winterfell', u'Valar Morghulis',
        u'What Is Dead May Never Die']

    """

    season_eps = Episode.query.filter(Episode.ep_season == season).all()

    ep_names = []

    for ep in season_eps:
        ep_names.append(ep.ep_name)

    return sorted(ep_names)


##########################################
# House searches


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
