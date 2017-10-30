# BoardGameGeek-DataScience

This repo contains Python scripts that involve web scraping and eventually data analytics, machine learning, and visualization. 

The project is based around the data provided by Board Game Geek (https://www.boardgamegeek.com)

## Quirky Things I Have Found in the Data So Far...

__Note__: Some data are poll based and therefore can change over time as more people contribute to a boardgame's data by voting in polls. Therefore my data is collected from a frozen point in time; things will surely change if I were to scrape again in a month, a year, etc.

* One game was published in the year 3500 BC! It was an ancient Egyptian game called Senet (https://boardgamegeek.com/boardgame/2399/senet). There are many games on boardgamegeek.com that span across the centuries, such as Chess (1475 AD).

* One game has a suggested age of 42+ for players! (https://boardgamegeek.com/boardgame/97683/south-african-railroads). Although only one/two people have voted on the suggested age poll for this boardgame, the vote was cast at 14+ years old.

## Description of Python Scripts 

### collect_games.py

This crawls across the pages of Board Game Geek that contain lists of board games, providing 100 games per page and listed in order of their current Geek Rating. This script grabs some simple info on the games and stores them in a csv file.

BGG_GameList_tabbed.csv is an example of the file output by:

```
import collect_games

collect_games.scrape_list_of_top_games(num_games= 10000, out_file_name = 'BGG_GameList_tabbed.csv')
```
 
### bg_scraper.py

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

### normalize_database.py

Since 6 columns in the boardgames table contain text arrays, it makes it significantly more difficult to query based on those columns. Therefore this script normalizes the database by creating 6 separate tables for those 6 columns.

Columns turned into new tables:
* designers
* artists
* categories
* mechanics
* family
* type

This script can be run from the command line and it will go through and make all 6 tables. The user could also import the script and run the functions individually. 

```
$ python normalize.py
```

### data_analysis.py

This contains a plethora of functions which access the database and provide data for analysis. Will constantly be growing with new functions as I find new things to investigate.