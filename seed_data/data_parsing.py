

# Game of Thrones
# https://api.got.show/doc/

# IMDB
# https://www.omdbapi.com/

# Etsy
# https://www.etsy.com/developers/documentation/getting_started/api_basics


import json



********* CHAR *********


json_string = open("chars.json").read()
char_dict = json.loads(json_string)

        for char in char_dict:
            print "(%s, %s, %s, %s)" % (char['name'], char['male'], char.get('house', 'NULL'), char['titles'])


********* EP ************


json_string = open("episodes.json").read()
episodes_dict = json.loads(json_string)



********* LOC *************


json_string = open("locations.json").read()
location_dict = json.loads(json_string)

loc_set = set()
for loc in location_dict:
    for l in loc['locations']:
        loc_set.add(l)


********* PATH ************


json_string = open("paths.json").read()
paths_dict = json.loads(json_string)

        for path in paths_dict:
            print path['name'], path['path'][-1]['alive']


********* TITLE *********

json_string = open("paths.json").read()
paths_dict = json.loads(json_string)






#######DATA MODELING #######

# *** All chars: ***

#     {u'male': False,
#      u'titles': [],
#     u'name': u'Zia Frey',
#     u'house': u'House Frey',
#     u'pageRank': 7.5,
#     u'dateOfBirth': 285, u'__v': 0,
#     u'books': [u'A Clash of Kings', u'A Storm of Swords', u'A Feast for Crows'],
#     u'updatedAt': u'2016-04-02T13:14:40.614Z',
#     u'_id': u'56ffc5c00432440819385f59',
#     u'slug': u'Zia_Frey',
#     u'createdAt': u'2016-04-02T13:14:40.614Z'}

# 1 char_id
# 2 = name
# 3 = male
# 4 = house
# 5= titles


# *** Locations: ***

# {u'locations': [u'Harrenhal', u'Maidenpool'],
# u'_id': u'56faa17c4cee25046571da68',
# u'slug': u'Zollo',
# u'__v': 0,
# u'name': u'Zollo'}]

# 1 = Loc_id
# 2 = location:[]

# 2 = char_name


# *** Episodes: ***

# {u'predecessor': u'The Dance of Dragons',
#  u'name': u"Mother's Mercy",
# u'airDate': u'2015-06-14T04:00:00.000Z',
# u'totalNr': 50,
# u'updatedAt': u'2016-03-30T12:52:14.551Z',
# u'director': u'David Nutter',
# u'__v': 2,
# u'characters': [u'Theon Greyjoy', u'Grey Worm', u'Mace Tyrell', u'Talla Tarly', u'Gregor Clegane', u'Walder Frey',
# u'Samwell Tarly', u'Obara Sand', u'Brienne of Tarth', u'Daenerys Targaryen', u'Jaime Lannister', u'Eddison Tollett',
# u'Davos Seaworth', u'Tyrion Lannister', u'Margaery Tyrell', u'Missandei', u'Randyll Tarly', u'Bronn', u'Othell Yarwyck',
# u'Kevan Lannister', u'Amarei Crakehall', u'Petyr Baelish', u'Jorah Mormont', u'Jon Snow', u'Cersei Lannister', u'Nymeria Sand',
# u'Daario Naharis', u'Loras Tyrell', u'Meera Reed', u'Tyene Sand', u'Roose Bolton', u'Edmure Tully', u'Gilly', u'Hodor',
# u'Holly', u'Areo Hotah', u'Rickon Stark', u'Podrick Payne', u'High Sparrow', u'Brynden Tully', u'Trystane Martell',
# u'Doran Martell', u'Lancel Lannister', u'Melessa Florent', u'Dickon Tarly', u'Alliser Thorne', u'Osha', u'Sansa Stark',
# u'Melisandre', u'Ellaria Sand', u'Arya Stark', u"Jaqen H'ghar", u'Bran Stark', u'Euron Greyjoy', u'Tommen Baratheon'],
# u'season': 5,
# u'nr': 10,
# u'_id': u'56fa9944b528554c6493b7e2',
# u'createdAt': u'2016-03-29T15:03:32.719Z'}]

# 1 = name (as ep_name)
# 2 = season (as ep_season)
# 3 =  characters []

# *** Paths ***

# {u'path': [[45.805474068515245, -84.48536531890602, u"King's Landing"]],
# u'from': 47,
# u'alive': True}],
# u'_id': u'56ffc726aa02d99219e0612b',
# u'name': u'Petyr Baelish',
# u'__v': 0}

#1 = name
#2 = alive

