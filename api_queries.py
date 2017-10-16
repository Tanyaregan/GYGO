
import requests
from pprint import pprint
import os

ETSY_API_KEY = os.environ['ETSY_API_KEY']

# Wikia searches
##################################################################


def search_term_char_name(char):
    """Reformats search name to correctly work with wikia api."""

    char_name = []

    for letter in char:
        if letter == ' ':
            letter = '_'
            char_name.append(letter)
        else:
            char_name.append(letter)

    return ('').join(char_name)


def wikia_char_article_id(char_name):
    """Searches wikia with char_name, returns top article_id."""

    payload = {'query': char_name}

    articles = requests.get('http://gameofthrones.wikia.com/api/v1/Search/List/', params=payload)

    if articles.ok:

        articles_dict = articles.json()

        wik_char_id = articles_dict["items"][0]["id"]

        return wik_char_id

    else:

        return None


def wikia_char_thumb(wik_char_id):
    """Searches article info, returns thumbnail link and abstract."""

    if wik_char_id:

        payload = {'ids': wik_char_id}

        article_details = requests.get('http://gameofthrones.wikia.com/api/v1/Articles/Details/', params=payload)

        article_detail_dict = article_details.json()

        article_items_detail = article_detail_dict.get("items", {})

        char_thumb_url = article_items_detail[str(wik_char_id)]['thumbnail']

        return char_thumb_url

    else:

        return None

# Etsy search
################################################################################


def etsy_sale_search(char_name):
    """Searches Etsy with "GoT" + char_name to return sale items."""

    payload = {'api_key': ETSY_API_KEY, 'limit': 5, 'category': 'clothing',
               'keywords': 'Game of Thrones ' + char_name, 'fields': 'title,url, images',
               'includes': 'Images(url_170x135)', 'tags': 'game of thrones,costume,cosplay ' + char_name}

    items = requests.get('https://openapi.etsy.com/v2/listings/active/', params=payload)

    print "search url: ", items.url

    if items.ok:

        item_dict = items.json()

        for item in item_dict['results']:

            item_title = item['title']

            item_url = item['url']

            item_img = item['Images'][0]['url_170x135']

            print "item characteristics:"
            print "item title: ", item_title
            print "item url: ", item_url
            print "item img: ", item_img

    else:

        return None


# def wikia_char_abstract(wik_char_id):
#      """Searches article info, returns abstract text."""

#     payload = {'ids': wik_char_id, 'abstract': 500}

#     article_details = requests.get('http://gameofthrones.wikia.com/api/v1/Articles/Details/', params=payload)

#     article_detail_dict = article_details.json()

#     char_abstract = article_detail_dict["items"][str(wik_char_id)]["abstract"]

#     return char_abstract


# # Wikia searches - House
# #######################################################################


# def wikia_house_article_link(house_name):
#     """Searches wikia by house name, returns top article id."""

#     house_url = http://gameofthrones.wikia.com/wiki/house_name

#     return house_page_id


# def search_wikia_house_thumb(wik_house_id):
#     """Searches house info, returns sigil thumbnail url."""

#     return house_thumb_url


# def search_wikia_house_movie(wik_house_id):
#     """Searches house info, returns house movie url."""

#     return house_movie_url


# # Wikia Episode searches
# ######################################################################


# def search_term_ep_name(ep):
#     """Reformats search name to correctly work with api."""

#     ep_name = []

#     for letter in ep:
#         if letter == ' ':
#             letter = '_'
#             ep_name.append(letter)
#         else:
#             ep_name.append(letter)

#     return ('').join(ep_name)


# def wikia_episode_article_link(ep_name):
#     """Searches wikia and returns episode article_id."""

#         return wik_ep_id


# def wikia_ep_summary(wik_ep_id):
#     """Searches ep id, returns summary from wikia article."""

#         return ep_summary


# def wikia_search_ep_deaths(wik_ep_id):
#     """Searches ep id, returns death list from wikia article."""

#         return ep_deaths



