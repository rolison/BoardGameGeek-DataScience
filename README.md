# BoardGameGeek-DataScience

This repo contains Python scripts that involve web scraping and eventually data analytics, machine learning, and visualization. 

The project is based around the data provided by Board Game Geek (https://www.boardgamegeek.com)

__collect_games.py__

This crawls across the pages of Board Game Geek that contain lists of board games, providing 100 games per page and listed in order of their current Geek Rating. This script grabs some simple info on the games and stores them in a csv file.

BGG_GameList_tabbed.csv is an example of the file output by:

```
import collect_games

collect_games.scrape_list_of_top_games(num_games= 10000, out_file_name = 'BGG_GameList_tabbed.csv')
```
 
__bg_scraper.py__

This is the script that goes through the games provided in the csv file and gets much more detailed data on each game by using Board Game Geeks XML API

It grabs the data from the csv file in chunks, requests the detailed information about the games using the XML API, and then puts it into a Postgres database table. Now it can be grabbed anytime for data analysis.

This requires the user to set up a database named "bggdb". Or the user can edit the DATABASE variable inside the bg_scraper.py script so that it will correctly connect to their desired database on their system.

```
import bg_scraper

# Creates the table on the db which will store all game info
bg_scraper.create_table_in_database()

# Will request 100 games at a time from the XML API
bg_scraper.scrape_bg_stats(csv_file_name='BGG_GameList_tabbed.csv', chunk_size=100)
```
