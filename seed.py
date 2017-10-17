"""Utility file to seed database from GoT data in seed_data/."""

import json

import requests

from sqlalchemy import func

from model import Character, Title, Episode, House, CharTitle, CharEp, CharHouse
from model import connect_to_db, db

from api_queries import wikia_char_article_id

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

        char = Character(char_name=char_name,
                         char_male=char_male,
                         char_dead="Unknown")

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
        house = char.get('house')
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

                char_titles = CharTitle(char_id=char_id,
                                        title_id=title_id)

                db.session.add(char_titles)

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

                char_eps = CharEp(char_id=char_id,
                                  ep_id=ep_id)

                db.session.add(char_eps)

    db.session.commit()


def load_char_houses():
    """Load associative table with Character IDs and Houses."""

    print "Character-Houses..."

    CharHouse.query.delete()

    json_string = open("./seed_data/chars.json").read()
    char_house_dict = json.loads(json_string)

    for char in char_house_dict:

        house_name = char.get('house', 'No Affiliation')
        house_obj = House.query.filter(House.house_name == house_name).first()
        house_id = house_obj.house_id

        char_name = char['name']
        char_obj = Character.query.filter(Character.char_name == char_name).first()
        char_id = char_obj.char_id

        char_houses = CharHouse(char_id=char_id,
                                house_id=house_id)

        db.session.add(char_houses)

    db.session.commit()


#################################################
# Database cleaner functions


def char_names():
    """Returns list of char names"""

    char_objs = Character.query.order_by('char_name').all()

    char_names = []

    for char in char_objs:

        char_name = char.char_name

        char_names.append(char_name)

    return char_names


def non_wikia_chars(char_names):
    """Takes a list of char names with no wikia id,
    searches Wikia and adds name to list if not in Wikia."""

    non_wikia_char_names = []

    for char in char_names:

        if not wikia_char_article_id(char):

            non_wikia_char_names.append(char)

    return non_wikia_char_names


def non_wikia_char_ids(non_wikia_char_names):
    """takes a list of char names, returns char ids."""

    non_wikia_char_ids = []

    for name in non_wikia_char_names:

        char = Character.query.filter_by(char_name=name).first()

        char_id = char.char_id

        non_wikia_char_ids.append(char_id)

    return non_wikia_char_ids


def delete_non_wikia_chars(non_wikia_char_ids):
    """Deletes all records from the non-wikia chars list."""

    for char_id in non_wikia_char_ids:

        char = CharHouse.query.filter_by(char_id=char_id).first()
        if char:
            db.session.delete(char)

        char = CharTitle.query.filter_by(char_id=char_id).first()
        if char:
            db.session.delete(char)

        char = CharEp.query.filter_by(char_id=char_id).first()
        if char:
            db.session.delete(char)

        char = Character.query.filter_by(char_id=char_id).first()
        if char:
            db.session.delete(char)

        db.session.commit()

        print "deleted char id", char_id


def delete_single_char_by_id(char_id):
    """Takes a char id and deletes rows from all tables in db."""

    char = CharHouse.query.filter_by(char_id=char_id).first()
    if char:
        db.session.delete(char)

    char = CharTitle.query.filter_by(char_id=char_id).first()
    if char:
        db.session.delete(char)

    char = CharEp.query.filter_by(char_id=char_id).first()
    if char:
        db.session.delete(char)

    char = Character.query.filter_by(char_id=char_id).first()
    if char:
        db.session.delete(char)

    db.session.commit()

    print char_id, "char deleted from 4 db tables"

    db.session.commit()


def delete_empty_houses():
    """Deletes rows in Houses where there is no chars in Char_house."""

    char_house_objs = CharHouse.query.order_by('house_id').all()
    char_house_ids = []

    for obj in char_house_objs:
        char_house_id = obj.house_id
        char_house_ids.append(char_house_id)

    house_objs = House.query.order_by('house_id').all()
    house_ids = []

    for obj in house_objs:
        house_id = obj.house_id
        house_ids.append(house_id)

    char_house_ids = set(char_house_ids)
    house_ids = set(house_ids)

    no_char_houses = house_ids - char_house_ids

    for house_id in no_char_houses:
        print house_id
        house_obj = House.query.filter_by(house_id=house_id).first()
        if house_obj:
            db.session.delete(house_obj)

    db.session.commit()


def delete_empty_titles():
    """Deletes rows in Titles where there is no chars in Char_title."""

    char_title_objs = CharTitle.query.order_by('title_id').all()
    char_title_ids = []

    for obj in char_title_objs:
        char_title_id = obj.title_id
        char_title_ids.append(char_title_id)

    title_objs = Title.query.order_by('title_id').all()
    title_ids = []

    for obj in title_objs:
        title_id = obj.title_id
        title_ids.append(title_id)

    char_title_ids = set(char_title_ids)
    title_ids = set(title_ids)

    no_char_titles = title_ids - char_title_ids

    for title_id in no_char_titles:

        title_obj = Title.query.filter_by(title_id=title_id).first()

        if title_obj:
            db.session.delete(title_obj)

    db.session.commit()



##################################################


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()


# load_characters()
# load_titles()
# load_episodes()
# load_houses()

# load_char_title()
# load_char_episodes()
# load_char_houses()

