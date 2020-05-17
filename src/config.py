#!/usr/bin/env python3
""" Module-wide constants"""


import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Wait time between AO3 requests in seconds
DELAY = 5

# Location of raw data dumps. Fandom subdirectories will be located here
DATA_PATH = '../data/raw/'
MODEL_PATH = '../models/'

INDICES_PREFIX = 'indices'
MODEL_PREFIX = 'implicit'
KUDO_PREFIX = 'kudos'
META_PREFIX = 'meta'
META_DB_PREFIX = 'meta_db'
KUDOS_DB_PREFIX = 'kudos_db'

LOG_SUFFIX = '.log'
DATA_SUFFIX = '.json'
PICKLE_SUFFIX = '.pkl'

# HTTP Request Headers
HTTP_HEADERS = {'User-Agent':
                'Scraping meta for fan analysis; rebecca.sanjabi@gmail.com'}

TEST_FANDOM_LIST = ["LEGO Star Wars: The Padawan Menace (Short Film)"]
'''
    "LEGO Star Wars - All Media Types",
    "LEGO Star Wars: The Complete Saga",
    "LEGO Star Wars: The Yoda Chronicles",
    "LEGO Star Wars: Droid Tales",
    "LEGO Star Wars: The Freemaker Adventures (Cartoon)",
,
    "LEGO Star Wars: The Empire Strikes Out (Short Film)",
    "Phineas and Ferb: Star Wars",
    "Star Wars Legends - All Media Types",
    "Star Wars Legends: Young Jedi Knights Series - Kevin J. Anderson & Rebecca Moesta",
    "Star Wars Legends: The Truce at Bakura - Kathy Tyers",
    "Star Wars Legends: Tales of the Jedi",
    "Star Wars Legends: Corellian Trilogy - Roger MacBride Allen",
    "Star Wars Legends: Hand of Thrawn Duology - Timothy Zahn",
    "Star Wars Legends: Black Fleet Crisis Trilogy - Michael P. Kube-McDowell",
    "Star Wars Legends: Crucible - Troy Denning",
    "Star Wars Legends: Darth Plagueis - James Luceno",
    "Star Wars Legends: Fate of the Jedi Series - Aaron Allston & Troy Denning & Christie Golden",
    "Star Wars Legends: Force Unleashed - All Media Types",
    "Star Wars Legends: Jedi Quest Series - Jude Watson",
    "Star Wars Legends: Last of The Jedi Series - Jude Watson",
    "Star Wars Legends: Outbound Flight - Timothy Zahn",
    "Star Wars Legends: Republic (Comics)",
    "Star Wars Legends: Secrets of the Jedi - Jude Watson",
    "Star Wars Legends: The Lando Calrissian Adventures Series - L. Neil Smith",
    "Star Wars Legends: Knights of the Old Republic (Comic)",
    "Star Wars Legends: Legacy of the Force Series - Aaron Allston & Troy Denning & Karen Traviss",
    "Star Wars Legends: Thrawn Trilogy - Timothy Zahn",
    "Star Wars Legends: Republic Commando Series - Karen Traviss",
    "Star Wars Legends: X-Wing Series - Aaron Allston & Michael Stackpole",
    "Star Wars Legends: Jedi Apprentice Series - Jude Watson & Dave Wolverton",
    "Star Wars Legends: Shadows of the Empire - Steve Perry",
    "Star Wars Legends: I Jedi - Michael A. Stackpole",
    "Star Wars Legends: Allegiance - Timothy Zahn",
    "Star Wars: Darth Maul (Comics)",
    "Star Wars Legends: Dark Nest Trilogy - Troy Denning",
    "Star Wars Legends: Dawn of the Jedi (Comics)",
    "Star Wars Legends: Yoda: Dark Rendezvous - Sean Stewart",
    "Star Wars Legends: Jedi Academy Trilogy - Kevin J. Anderson",
    "Star Wars Legends: Darth Bane Trilogy - Drew Karpyshyn",
    "Star Wars Legends: Jedi vs. Sith (Comic)",
    "Star Wars Legends: Galaxies (Video Game)",
    "Star Wars Legends: Kenobi - John Jackson Miller",
    "Star Wars Legends: Ewoks (Cartoon)",
    "Star Wars Legends: New Jedi Order Series - Various Authors",
    "Star Wars Legends: The Old Republic (Video Game)",
    "Star Wars Legends: Knights of the Old Republic (Video Games)",
    "Star Wars Legends: Legacy (Comics)",
    "Star Wars Legends: Maul: Lockdown - Joe Schreiber",
    "Star Wars Legends: Jedi Knight (Video Games)",
    "Star Wars Legends: Republic Commando (Video Games)",
    "Star Wars Legends: Darth Vader and the Ghost Prison (Comics)",
    "Star Wars Legends: The Courtship of Princess Leia - Dave Wolverton",
    "Star Wars Legends: The Old Republic Series - Drew Karpyshyn & Paul S. Kemp & Sean Williams",
    "Star Wars Legends: Junior Jedi Knights Series - Nancy Richardson & Rebecca Moesta",
    "Star Wars Legends: Red Harvest - Joe Schreiber",
    "Star Wars Legends: Children of the Jedi - Barbara Hambly",
    "Star Wars Legends: Rogue Squadron (Video Games)",
    "Star Wars: Tarkin - James Luceno",
    "Star Wars Sequel Trilogy",
    "Star Wars (Marvel Comics)",
    "Star Wars: Princess Leia (Comics)",
    "Star Wars: Darth Vader (Comics)",
    "Star Wars: Shattered Empire",
    "Star Wars: Lando (Comics)",
    "Star Wars: Poe Dameron (Comics)",
    "Star Wars: Jedi of the Republic – Mace Windu (Comics)",
    "Journey to Star Wars: The Force Awakens",
    "Star Wars: Aftermath - Chuck Wendig",
    "Star Wars: Shattered Empire",
    "Star Wars: Before the Awakening - Greg Rucka",
    "Star Wars: Lost Stars - Claudia Gray",
    "Star Wars: Bloodline - Claudia Gray",
    "Star Wars: Battlefront (Video Games)",
    "Star Wars: Doctor Aphra (Comics)",
    "Star Wars: Phasma - Delilah S. Dawson",
    "Star Wars: The Legends of Luke Skywalker - Ken Liu",
    "Solo: A Star Wars Story (2018)",
    "Star Wars: Most Wanted - Rae Carson",
    "Star Wars: Leia Princess of Alderaan - Claudia Gray",
    "Star Wars: Thrawn Series - Timothy Zahn (2017)",
    "Star Wars: The Mighty Chewbacca in the Forest of Fear - Tom Angleberger",
    "Star Wars: Forces of Destiny (Web Series)",
    "Star Wars: Most Wanted - DJ",
    "Star Wars: Chewie and the Porgs - Kevin Shinick",
    "Star Wars: Resistance (Cartoon)",
    "Star Wars: Canto Bight - Various Authors",
    "The Mandalorian (TV)",
    "Star Wars: Master and Apprentice - Claudia Gray",
    "Star Wars: Jedi: Fallen Order (Video Game)",
    "Star Wars: Alphabet Squadron Series - Alexander Freed",
    "Star Wars: Age of Resistance (Comics)",
    "Star Wars: Kanan (Comics)",
    "Star Wars: Galaxy's Edge: Black Spire - Delilah S. Dawson",
    "Star Wars: From a Certain Point of View - Various Authors",
    "Star Wars: Queen's Shadow - E. K. Johnston",
    "Star Wars: Allegiance (Comics)",
    "Star Wars: Resistance Reborn - Rebecca Roanhorse",
    "Star Wars: Adventures in Wild Space - Tom Huddleston & Cavan Scott",
    "Star Wars: The Rise of Kylo Ren (Comics)",
    "Star Wars: Galaxy's Edge (Attraction)"]
'''

# How many attempts at requesting page before quitting
MAX_ERRORS = 3

HOST = 'ec2-52-23-14-156.compute-1.amazonaws.com'

META_COLS = ['work_id', 'title', 'author', 'gifted', 'rating', 'warnings',
             'category', 'status', 'fandom', 'relationship', 'characters',
             'freeforms', 'summary', 'language', 'words', 'chapters',
             'collections', 'comments', 'kudos', 'bookmarks', 'hits',
             'series_part', 'series_name', 'updated', 'scrape_date']

SCR_WINDOW = 21          # window for number of days before we rescrape kudos
