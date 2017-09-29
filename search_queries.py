from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from model import connect_to_db, Character, Title, Episode, CharTitle, CharEp

###########################################
# Search Functions


def search_by_name(name):
    """Searches db by char_name, pulls all associated info.

        >>> search_by_name('Gilly')
        {'char_dead': u'Not yet',
         'char_eps': [u'Fire and Blood',
          u'The North Remembers',
          u'The Night Lands',
          u'Dark Wings, Dark Words',
          u'Walk of Punishment',
          u'Kissed by Fire',
          u'Second Sons',
          u'The Bear and the Maiden Fair',
          u'The Rains of Castamere',
          u'The Lion and the Rose',
          u'Mockingbird',
          u'The Mountain and the Viper',
          u'The Children',
          u'The Wars to Come',
          u'Sons of the Harpy',
          u'Unbowed, Unbent, Unbroken',
          u'The Gift',
          u'The Dance of Dragons',
          u"Mother's Mercy"],
         'char_house': u'No Affiliation',
         'char_male': False,
         'char_name': 'Gilly',
         'char_num': 647,
         'char_titles': []}


        >>> search_by_name('Aemond Targaryen')
        {'char_dead': u'Totally',
         'char_eps': [],
         'char_house': u'House Targaryen',
         'char_male': True,
         'char_name': 'Aemond Targaryen',
         'char_num': 29,
         'char_titles': [u'Prince', u'Protector of the Realm', u'Prince Regent']}



    """

    char_obj = Character.query.filter(Character.char_name == name).first()

    # Basic character info:

    char_num = char_obj.char_id
    char_name = name
    char_male = char_obj.char_male
    char_house = char_obj.char_house
    char_dead = char_obj.char_dead

    # Title list:

    title_list_obj = CharTitle.query.filter(CharTitle.char_id == char_num).all()

    char_titles = []

    for title in title_list_obj:
        title_num = title.title_id
        title = Title.query.filter(Title.title_id == title_num).first()
        char_titles.append(title.title_name)

    # Episode list:

    ep_list_obj = CharEp.query.filter(CharEp.char_id == char_num).all()

    char_eps = []

    for ep in ep_list_obj:
        ep_num = ep.ep_id
        ep = Episode.query.filter(Episode.ep_id == ep_num).first()
        char_eps.append(ep.ep_name)

    # Populate info dictionary:

    char_info = {}

    char_info['char_num'] = char_num
    char_info['char_name'] = char_name
    char_info['char_male'] = char_male
    char_info['char_dead'] = char_dead
    char_info['char_house'] = char_house
    char_info['char_titles'] = char_titles
    char_info['char_eps'] = char_eps

    return char_info
    print char_info


def search_by_gender(gender):
    """Searches db by char_male, returns char_ids for all of that gender.

    """

    pass


def search_by_dead(dead):
    """Searches db by char_dead, returns char_ids for all who have that title.

    """

    pass


def search_by_title(title):
    """Searches db by a title, returns char_ids for all who have that title.

    """

    pass


def search_by_house(house):
    """Searches db by house, returns char_ids for all chars in that house.

    """

    pass


def search_by_episode(episode):
    """Searches db by episode name, returns char_ids for all chars in that episode.

    """

    pass


def search_by_season(season):
    """Searches db by season number, returns all episodes in that season.

    """

    pass


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
