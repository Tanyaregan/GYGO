"""Utility file to seed database from GoT data in seed_data/."""

import json

from sqlalchemy import func

from model import Character, Title, Episode, House, CharTitle, CharEp, CharHouse
from model import connect_to_db, db

from server import app


##############################################
#Load Primary Tables


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
                         char_dead="Not yet..")

        db.session.add(char)

    db.session.commit()


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


def load_houses():
    """Load houses from seed_data/characters into database."""

    print "Houses..."

    House.query.delete()

    json_string = open("./seed_data/chars.json").read()
    chars_dict = json.loads(json_string)

    house_set = set()

    for char in chars_dict:
        for house in char.get('house'):
            house_set.add(house)

    for house_name in house_set:

        house = House(house_name=house_name)

        db.session.add(house)

    db.session.commit()

###############################################
# Load Associative Tables


def load_char_title():
    """Load associative table with Character IDs and Titles."""

    print "Character-Titles..."

    CharTitle.query.delete()

    json_string = open("./seed_data/chars.json").read()
    char_title_dict = json.loads(json_string)

    for char in char_title_dict:

        if char['titles']:

            char_name = char['name']
            char_obj = Character.query.filter(Character.char_name == char_name).first()
            char_id = char_obj.char_id

            for title_name in char['titles']:

                title_obj = Title.query.filter(Title.title_name == title_name).first()

                if title_obj is None:
                    continue

                title_id = title_obj.title_id

                char_title = CharTitle(char_id=char_id,
                                       title_id=title_id)

                db.session.add(char_title)

        else:
            pass

    db.session.commit()


def load_char_episodes():
    """Load associative table with Character IDs and Episodes."""

    print "Character-Episodes..."

    CharEp.query.delete()

    json_string = open("./seed_data/episodes.json").read()
    char_ep_dict = json.loads(json_string)

    for ep in char_ep_dict:

            for char in ep['characters']:

                char_obj = Character.query.filter(Character.char_name == char).first()
                char_id = char_obj.char_id

                ep_name = ep['name']
                ep_obj = Episode.query.filter(Episode.ep_name == ep_name).first()
                ep_id = ep_obj.ep_id

                char_ep = CharEp(char_id=char_id,
                                 ep_id=ep_id)

                db.session.add(char_ep)

    db.session.commit()


def load_char_houses():
    """Load associative table with Character IDs and Houses."""

    print "Character-Houses..."

    CharHouse.query.delete()

    json_string = open("./seed_data/chars.json").read()
    char_house_dict = json.loads(json_string)

    for char_obj in char_house_dict:

        char_id = char_obj.char_id

        house_name = char_obj['char_house']
        house_obj = House.query.filter(House.house_name == house_name).first()
        house_id = house_obj.house_id

        char_house = CharHouse(char_id=char_id,
                               house_id=house_id)

        db.session.add(char_house)

##################################################

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()


load_characters()
load_titles()
load_episodes()
load_houses()

# load_char_title()
# load_char_episodes()
# load_char_houses()
