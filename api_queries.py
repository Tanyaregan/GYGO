
import requests
import os

from ebaysdk.finding import Connection as Finding

ETSY_API_KEY = os.environ['ETSY_API_KEY']
EBAY_API_KEY = os.environ['EBAY_API_KEY']

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

# Etsy searches
################################################################################


def etsy_search(char_name, limit):
    """Searches Etsy with associated payload paraameters."""

    payload = {'api_key': ETSY_API_KEY, 'limit': limit, 'category': 'clothing',
               'keywords': 'Game of Thrones ' + char_name, 'fields': 'title,url,immages',
               'includes': 'Images(url_170x135)',
               'tags': 'game of thrones,costume,cosplay ' + char_name}

    items = requests.get('https://openapi.etsy.com/v2/listings/active/', params=payload)

    if items.ok:

        item_dict = items.json()

        etsy_item_objs = []

        for item in item_dict['results']:

            item_obj = {}

            item_title = item['title']
            item_obj['title'] = item_title

            item_url = item['url']
            item_obj['url'] = item_url

            item_img = item['Images'][0]['url_170x135']
            item_obj['thumb'] = item_img

            etsy_item_objs.append(item_obj)

    else:

        return None

    return etsy_item_objs


def char_page_etsy(char_name):
    """Searches Etsy to return 3 sale items."""

    char_etsy_items = etsy_search(char_name, 3)

    return char_etsy_items


def item_page_etsy(char_name):
    """Searches Etsy to return 15 sale items."""

    char_etsy_items = etsy_search(char_name, 15)

    return char_etsy_items


# Ebay searches
########################################################################

def ebay_search(char_name, pagination):
    """Searches ebay with associated payload parameters."""

    api_request = {'keywords': 'Game of Thrones ' + char_name, 'categoryId': 175648,
                   'paginationInput': pagination,
                   'HideDuplicateItem': True}

    try:

        api = Finding(appid=EBAY_API_KEY, config_file=None)
        response = api.execute('findItemsAdvanced', api_request)
        ebay_results = response.dict()

    except:

        print "Got nothin"

    data_present = ebay_results['searchResult'].get('item', None)

    if data_present:

        ebay_items = []

        for item in ebay_results['searchResult']['item']:

            ebay_item = {}

            thumb = item['galleryURL']
            title = item['title']
            url = item['viewItemURL']

            ebay_item['thumb'] = thumb
            ebay_item['title'] = title
            ebay_item['url'] = url

            ebay_items.append(ebay_item)

    else:

        return None

    return ebay_items


def char_page_ebay(char_name):
    """Searches Ebay with 3 item pagination."""

    char_ebay_items = ebay_search(char_name, {'entriesPerPage': 3, 'pageNumber': 2})

    return char_ebay_items


def item_page_ebay(char_name,):
    """Searches Ebay with 15 item pagination."""

    item_ebay_items = ebay_search(char_name, {'entriesPerPage': 15, 'pageNumber': 1})

    return item_ebay_items

###########################################
# Doc Tests

if __name__ == "__main__":
    print
    import doctest
    if doctest.testmod().failed == 0:
        print "*** PASSED! (woot) ***"
    print

