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

The plan is to grab the data and put it into a Postgres database, which can then be grabbed anytime for data analysis.
