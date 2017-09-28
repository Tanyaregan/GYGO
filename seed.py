"""Utility file to seed database from GoT data in seed_data/."""

import json

from sqlalchemy import func

from model import Character, Title, Episode, EpChar, TitleChar
from model import connect_to_db, db

from server import app


##############################################


def load_characters():
    """Load chars from seed_data/characters into database."""

    print "Characters..."

    Character.query.delete()

    json_string = open("./seed_data/chars.json").read()
    chars_dict = json.loads(json_string)

    for char in chars_dict:
        char_name = char['name']
        char_male = char['male']
        char_house = char.get('house', 'NULL')

        char = Character(char_name=char_name,
                         char_male=char_male,
                         char_house=char_house,
                         char_alive=None)

        db.session.add(char)

    db.session.commit()


##############################################


def load_titles():
    """Load titles from seed_data/characters into database."""

    print "Titles..."

    Title.query.delete()

    json_string = open("./seed_data/chars.json").read()
    chars_dict = json.loads(json_string)

    title_set = set()

    for char in chars_dict:
        for title in char.get('titles'):
            title_set.add(title)

    for title_name in title_set:

        title = Title(title_name=title_name)

        db.session.add(title)

    db.session.commit()


##############################################


def load_episodes():
    """Load episodes from seed_data/episodes into database."""

    print "Episodes..."

    Episode.query.delete()

    json_string = open("./seed_data/episodes.json").read()
    eps_dict = json.loads(json_string)

    for ep in eps_dict:
        ep_name = ep['name']
        ep_season = ep['season']

        ep = Episode(ep_season=ep_season,
                     ep_name=ep_name)

        db.session.add(ep)

    db.session.commit()


###############################################


def load_titlechar():
    """Load associative table with Titles and Character IDs."""

    print "Title-Characters..."

    TitleChar.query.delete()

    json_string = open("./seed_data/chars.json").read()
    title_char_dict = json.loads(json_string)

    for char in title_char_dict:

        if char['titles']:

            char_name = char['name']
            char_obj = Character.query.filter(Character.char_name == char_name).first()
            char_id = char_obj.char_id

            for title_name in char['titles']:

                title_obj = Title.query.filter(Title.title_name == title_name).first()

                if title_obj is None:
                    continue

                title_id = title_obj.title_id

                title_char = TitleChar(char_id=char_id,
                                       title_id=title_id)

                db.session.add(title_char)

        else:
            pass

    db.session.commit()


###############################################


def load_epchar():
    """Load associative table with Episodes and Character IDs."""

    print "Episode-Characters..."

    EpChar.query.delete()

    json_string = open("./seed_data/episodes.json").read()
    ep_char_dict = json.loads(json_string)

    for ep in ep_char_dict:

            for char in ep['characters']:

                char_obj = Character.query.filter(Character.char_name == char).first()
                char_id = char_obj.char_id
                ep_name = ep['name']

                ep_obj = Episode.query.filter(Episode.ep_name == ep_name).first()
                ep_id = ep_obj.ep_id

                ep_char = EpChar(char_id=char_id,
                                 ep_id=ep_id)

                db.session.add(ep_char)

    db.session.commit()



##################################################

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()


# load_characters()
# load_titles()
# load_episodes()

# load_titlechar()
# load_epchar()
