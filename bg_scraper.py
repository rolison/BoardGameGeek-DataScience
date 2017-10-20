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

# Global Variables

WAIT_TIME_BETWEEN_REQUESTS = 6 # seconds

BGG_XMLAPI = 'https://www.boardgamegeek.com/xmlapi/boardgame/'

def create_database():
    pass

def add_to_database(board_game):
    pass

def scrape_bg_stats(csv_file_name, chunk_size, num_bgs = None):
    '''
    csv_file_name = Name of the csv file that was created inside the 
                    collect_games.py script
                    (string)

    chunk_size    = The number of boardgames to request in a single XMLAPI call
                    (int)

    num_bgs       = If you don't want every single game in the csv file to be
                    scraped, provide an integer telling it the total amount.
                    (int)
    '''

    # Holds list of boardgames to be scraped, will be of length "chunk_size"
    bg_list = []

    # Keeping track of how many chunks of boardgames are being scraped
    i = 0

    with open(csv_file_name, 'rb') as csv_file:

        csv_contents = csv.reader(csv_file, delimiter = '\t')

        labels = csv_contents.next()

        for row in csv_contents:

            if len(bg_list) == chunk_size:

                i += 1

                if num_bgs:

                    print "Scraping chunk", i, "of", num_bgs/chunk_size

                else:

                    print "Scraping chunk", i, "of", 10000/chunk_size

                scrape_list_of_games(labels, bg_list)

                # Clear list so we can build up another chunk
                bg_list = []

                bg_list.append(row)

                time.sleep(WAIT_TIME_BETWEEN_REQUESTS)

            else:

                bg_list.append(row)

            # Add 1 to stop index since generator already moved line_num by 1
            if num_bgs is not None and csv_contents.line_num > num_bgs + 1:

                return

def scrape_list_of_games(labels, bg_list):

    bg_index = labels.index('HRef')

    # Make a list of just the board game ID's
    bgID_list = [bgame[bg_index].split('/')[2] for bgame in bg_list]

    games = ','.join(bgID_list)
    
    r = requests.get(BGG_XMLAPI + games + '?stats=1')

    soup = BeautifulSoup(r.text, 'xml')

    for boardgame in soup.boardgames:

        scrape_game(boardgame)

def scrape_game(boardgame):
    
    pass


def _grab_single_value_from_tag_object(tag_obj, data_type):

    try:

        return data_type(tag_obj.contents[0])

    except AttributeError:

        return None

def _grab_multiple_values_from_tag_object(tag_obj_list, data_type):

    return [data_type(tag.contents[0]) for tag in tag_obj_list]

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