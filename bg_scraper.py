'''
- Use BGG's XML API to get data on list of board games
- Scrape all the data from it
- Store it in database
'''

import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import csv
import psycopg2
from psycopg2 import IntegrityError, InternalError

# Global Variables

WAIT_TIME_BETWEEN_REQUESTS = 2 # seconds

BGG_XMLAPI = 'https://www.boardgamegeek.com/xmlapi/boardgame/'

DATABASE = "dbname = 'bggdb'" # edit this if you need more info to connect to db


def create_table_in_database():

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            curs.execute("""CREATE TABLE boardgame (
                                    id int PRIMARY KEY,
                                    rank           int,
                                    name          text,
                                    href          text,
                                    pub_year       int,
                                    geek_rating   real,
                                    avg_rating    real,
                                    num_voters     int,
                                    min_players    int,
                                    max_players    int,
                                    play_time      int,
                                    sugg_age       int, -- suggested age
                                    complx_rating real, -- complexity rating
                                    designers   text[],
                                    artists     text[],
                                    categories  text[],
                                    mechanisms  text[],
                                    family      text[],
                                    type        text[]
                                    );""")

            print "Table succesfully created"

def scrape_bg_stats(csv_file_name, chunk_size, num_bgs = None, db=DATABASE):
    '''
    csv_file_name = Name of the csv file that was created inside the 
                    collect_games.py script
                    (string)

    chunk_size    = The number of boardgames to request in a single XMLAPI call
                    (int)

    num_bgs       = If you don't want every single game in the csv file to be
                    scraped, provide an integer telling it the total amount.
                    (int)

    db            = name of the database to connect to
    '''

    # Holds list of boardgames to be scraped, will be of length "chunk_size"
    bg_list = []

    # Keeping track of how many chunks of boardgames are being scraped
    i = 0

    # Keeping track of how many erroneously labeled games had to be skipped
    total_skipped = 0

    with open(csv_file_name, 'rb') as csv_file:

        csv_contents = csv.reader(csv_file, delimiter = '\t')

        labels = csv_contents.next()

        for row in csv_contents:

            if len(bg_list) == chunk_size:

                i += 1

                if num_bgs:

                    print "\nScraping chunk", i, "of", num_bgs/chunk_size

                else:

                    print "\nScraping chunk", i, "of", 10000/chunk_size

                total_skipped += scrape_list_of_games(labels, bg_list, db)

                # Clear list so we can build up another chunk
                bg_list = []

                bg_list.append(row)

                time.sleep(WAIT_TIME_BETWEEN_REQUESTS)

            else:

                bg_list.append(row)

            # Add 1 to stop index since generator already moved line_num by 1
            if num_bgs is not None and csv_contents.line_num > num_bgs + 1:

                print "\nTotal Number of Erroneously Labeled Games Skipped:",\
                                                               total_skipped
                return

        # For last chunk in csv file that may reach end of file midway
        else:

            i += 1

            if num_bgs:

                print "\nScraping chunk", i, "of", num_bgs/chunk_size

            else:

                print "\nScraping chunk", i, "of", 10000/chunk_size

            total_skipped += scrape_list_of_games(labels, bg_list, db)

    print "\nTotal Number of Erroneously Labeled Games Skipped:", total_skipped

def scrape_list_of_games(labels, bg_list, db):

    bg_index = labels.index('HRef')

    # Make a list of just the board game ID's
    bgID_list = [bgame[bg_index].split('/')[2] for bgame in bg_list]

    games = ','.join(bgID_list)
    
    r = requests.get(BGG_XMLAPI + games + '?stats=1')

    soup = BeautifulSoup(r.text, 'xml')

    games_skipped = 0
        
    with psycopg2.connect(db) as conn:
        with conn.cursor() as cursor:

            for boardgame in soup.boardgames.find_all('boardgame'): 

                # Found weird bug where some items were listed as games inside
                #   XML API. Used this conditional to make sure it's only
                #   picking up games that are actually documented
                if boardgame.attrs['objectid'] not in bgID_list:

                    games_skipped += 1

                else: 

                    # Since we lost the index due to possible erroneously
                    #    labeled games
                    bg_index = bgID_list.index(boardgame.attrs['objectid'])
                    
                    bgID     = bgID_list[bg_index]

                    csv_row  = bg_list[bg_index]

                    bg_dict = scrape_game(boardgame, csv_row, bgID)

                    add_to_table(cursor, bg_dict)

    print "Erroneously Labeled Games Skipped This Chunk:", games_skipped

    return games_skipped
                    

def scrape_game(boardgame, csv_row, bgID):

    bg_dict = {}
    
    bg_dict['id']            = bgID
    bg_dict['rank']          = csv_row[0]
    bg_dict['name']          = csv_row[1]
    bg_dict['href']          = csv_row[2]
    bg_dict['pub_year']      = csv_row[3] if csv_row[3] != 'N/A' else None
    bg_dict['geek_rating']   = csv_row[4] if csv_row[4] != 'N/A' else None
    bg_dict['avg_rating']    = csv_row[5] if csv_row[5] != 'N/A' else None
    bg_dict['num_voters']    = csv_row[6] if csv_row[6] != 'N/A' else None
    bg_dict['min_players']   = boardgame.minplayers.contents[0]
    bg_dict['max_players']   = boardgame.maxplayers.contents[0]
    bg_dict['play_time']     = boardgame.playingtime.contents[0]
    bg_dict['sugg_age']      = boardgame.age.contents[0]
    bg_dict['complx_rating'] = boardgame.statistics.ratings.averageweight.contents[0]
    bg_dict['designers']     = [tag.contents[0] for tag in boardgame.find_all('boardgamedesigner')]
    bg_dict['artists']       = [tag.contents[0] for tag in boardgame.find_all('boardgameartist')]
    bg_dict['categories']    = [tag.contents[0] for tag in boardgame.find_all('boardgamecategory')]
    bg_dict['mechanisms']    = [tag.contents[0] for tag in boardgame.find_all('boardgamemechanic')]
    bg_dict['family']        = [tag.contents[0] for tag in boardgame.find_all('boardgamefamily')]
    bg_dict['type']          = [tag.contents[0] for tag in boardgame.find_all('boardgamesubdomain')]    

    return bg_dict

def add_to_table(cursor, bg_dict):

    cursor.execute("""INSERT INTO boardgames (
                                    id,
                                    rank,
                                    name,
                                    href,
                                    pub_year,
                                    geek_rating,
                                    avg_rating,
                                    num_voters,
                                    min_players,
                                    max_players,
                                    play_time,
                                    sugg_age,
                                    complx_rating,
                                    designers,
                                    artists,
                                    categories,
                                    mechanisms,
                                    family,
                                    type
                                    ) 
                                    VALUES (
                                    %(id)s,
                                    %(rank)s,
                                    %(name)s,
                                    %(href)s,
                                    %(pub_year)s,
                                    %(geek_rating)s,
                                    %(avg_rating)s,
                                    %(num_voters)s,
                                    %(min_players)s,
                                    %(max_players)s,
                                    %(play_time)s,
                                    %(sugg_age)s,
                                    %(complx_rating)s,
                                    %(designers)s,
                                    %(artists)s,
                                    %(categories)s,
                                    %(mechanisms)s,
                                    %(family)s,
                                    %(type)s
                                    ) ON CONFLICT DO NOTHING;""", bg_dict)

# Don't think I'll need this
def _grab_single_content(tag_obj):

    try:

        return tag_obj.contents[0]

    except AttributeError:

        return None

# Don't think I'll need this
def _grab_multiple_contents(tag_obj_list):

    try:

        return [tag.contents[0] for tag in tag_obj_list]

    except AttributeError:

        return None

# ============================================================================
# Functions that helped during debugging
# ============================================================================

def get_bg_xml(bgid):

    r = requests.get(BGG_XMLAPI + bgid + '?stats=1')

    soup = BeautifulSoup(r.text, 'xml')

    return soup

def grab_chunk_from_csv(csv_file_name, start, stop):

    bg_list = []

    with open(csv_file_name, 'rb') as csv_file:

        csv_contents = csv.reader(csv_file, delimiter = '\t')

        labels = csv_contents.next()

        for row in csv_contents:

            if csv_contents.line_num > start and csv_contents.line_num< stop + 1:

                bg_list.append(row)
    
    return bg_list

def make_game_id_list(bg_list):
    
    bgID_list = [bgame[2].split('/')[2] for bgame in bg_list]

    games = ','.join(bgID_list)

    return games

# Title -> csv file
# year published -> csv file
# rank data -> csv file
# Num Players  -> soup.boardgames.boardgame.minplayers.contents, soup.boardgames.boardgame.maxplayers.contents
# PlayTime -> soup.boardgames.boardgame.playingtime.contents
# Suggested Age -> soup.boardgames.boardgame.age.contents
# Complexity rating (out of 5) (lower means easier) -> soup.boardgames.boardgame.statistics.ratings.averageweight.contents

# !!! These all need to be grabbed as lists and iterated over to grab contents
# designers -> soup.boardgames.boardgame.find_all('boardgamedesigner')
# artist -> soup.boardgames.boardgame.find_all('boardgameartist')
# categories -> soup.boardgames.boardgame.find_all('boardgamecategory')
# mechanisms -> soup.boardgames.boardgame.find_all('boardgamemechanic')
# family ->  soup.boardgames.boardgame.find_all('boardgamefamily')
# type -> soup.boardgames.boardgame.find_all('boardgamesubdomain') , drop the 'Games' at end of each name

