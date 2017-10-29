import numpy as np
import csv
import psycopg2
import seaborn
import matplotlib.pyplot as plt
from bg_scraper import DATABASE # Global Variable

colors = seaborn.color_palette("deep")
seaborn.set_palette(colors)

def list_of_unique_items(column):
    '''
    Access database and create a list of all unique items in a specific 
    column from the boardgames table. Does this by accessing one of the
    tables made during database normalization (in normalize_data.py)

    Useful for the columns containing arrays of items that can occur 
    in multiple boardgames (artists, mechanics, type, etc.)

    Returns a list of unique column values
    '''

    sql_dict = {'designers' :"SELECT DISTINCT designer FROM designers;",
                'artists'   :"SELECT DISTINCT artist FROM artists;", 
                'categories':"SELECT DISTINCT category FROM categories;", 
                'mechanics' :"SELECT DISTINCT mechanic FROM mechanics;",
                'family'    :"SELECT DISTINCT family FROM families;", 
                'type'      :"SELECT DISTINCT type FROM types;"}

    if column not in sql_dict.keys():

        print "\nRequested column does not exist in table."
        print "Options for column:", sql_dict.keys()

        return

    item_list = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:
                
                curs.execute(sql_dict[column])

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to SELECT from table"

                return

            for row_tuple in curs.fetchall():
                    
                item_list.append(row_tuple[0])
    
    return item_list

def list_of_unique_items_for_rank(column, rank):
    '''
    Access database and create a list of all unique items in a specific 
    column from the boardgames table. Does this by accessing one of the
    tables made during database normalization (in normalize_data.py)

    Useful for the columns containing arrays of items that can occur 
    in multiple boardgames (artists, mechanics, type, etc.)

    Returns a list of unique column values that are within a top rank
    '''

    sql_dict = {'designers' :"""SELECT DISTINCT designer
                                FROM designers 
                                INNER JOIN boardgames 
                                ON boardgames.id=designers.bg_id 
                                WHERE boardgames.rank < %s;
                             """,
                'artists'   :"""SELECT DISTINCT artist
                                FROM artists 
                                INNER JOIN boardgames 
                                ON boardgames.id=artists.bg_id 
                                WHERE boardgames.rank < %s;
                             """, 
                'categories':"""SELECT DISTINCT category
                                FROM categories 
                                INNER JOIN boardgames 
                                ON boardgames.id=categories.bg_id 
                                WHERE boardgames.rank < %s;
                             """, 
                'mechanics' :"""SELECT DISTINCT mechanic
                                FROM mechanics 
                                INNER JOIN boardgames 
                                ON boardgames.id=mechanics.bg_id 
                                WHERE boardgames.rank < %s;
                             """,
                'family'    :"""SELECT DISTINCT family
                                FROM families 
                                INNER JOIN boardgames 
                                ON boardgames.id=families.bg_id 
                                WHERE boardgames.rank < %s;
                             """, 
                'type'      :"""SELECT DISTINCT type
                                FROM types 
                                INNER JOIN boardgames 
                                ON boardgames.id=types.bg_id 
                                WHERE boardgames.rank < %s;
                             """}

    if column not in sql_dict.keys():

        print "\nRequested column does not exist in table."
        print "Options for column:", sql_dict.keys()

        return

    item_list = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:
                
                curs.execute(sql_dict[column], (rank,))

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to SELECT from table"

                return

            for row_tuple in curs.fetchall():
                    
                item_list.append(row_tuple[0])
    
    return item_list

def count_column(column):
    '''
    Counts number of games associated with each unique value in a specified
    column.

    Uses the COUNT() and GROUP BY functionality of SQL language
    '''

    sql_dict = {'designers' :"""SELECT designer, COUNT(bg_id) FROM designers 
                                GROUP BY designer ORDER BY COUNT(bg_id) DESC;
                             """,
                'artists'   :"""SELECT artist, COUNT(bg_id) FROM artists
                                GROUP BY artist ORDER BY COUNT(bg_id) DESC;
                             """, 
                'categories':"""SELECT category, COUNT(bg_id) FROM categories
                                GROUP BY category ORDER BY COUNT(bg_id) DESC;
                             """, 
                'mechanics' :"""SELECT mechanic, COUNT(bg_id) FROM mechanics
                                GROUP BY mechanic ORDER BY COUNT(bg_id) DESC;
                             """,
                'family'    :"""SELECT family, COUNT(bg_id) FROM families
                                GROUP BY family ORDER BY COUNT(bg_id) DESC;
                             """, 
                'type'      :"""SELECT type, COUNT(bg_id) FROM types
                                GROUP BY type ORDER BY COUNT(bg_id) DESC;
                             """}

    if column not in sql_dict.keys():

        print "\nRequested column does not exist in table."
        print "Options for column:", sql_dict.keys()

        return

    item_list = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:
                
                curs.execute(sql_dict[column])

            except:

                print "Failed to SELECT from table"

                return

            for row_tuple in curs.fetchall():
                    
                item_list.append([row_tuple[0], int(row_tuple[1])])
    
    
    return item_list

def time_vs_max_players(time_cutoff = 1e10, player_cutoff = 1e10):
    '''
    Select games from boardgames that have a play_time less than the
    time_cutoff as well as a max_players below the player_cutoff.

    Returns two lists, one of the play_time's and one of max_players for
    the selected games
    '''

    time     = []
    max_plyr = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:
                
                curs.execute("""SELECT play_time, max_players 
                                FROM boardgames
                                WHERE play_time < %s AND max_players < %s;""",
                                (time_cutoff, player_cutoff))

            except:

                print "Failed to SELECT from table"

                return None,None

            for row_tuple in curs.fetchall():

                time.append(row_tuple[0])

                max_plyr.append(row_tuple[1])

    return time, max_plyr

def time_vs_complexity(time_cutoff = 1e10, cmplx_cutoff = 5):
    '''
    Select games from boardgames that have a play_time less than the
    time_cutoff as well as a complexity below the cmplx_cutoff.

    Returns two lists, one of the play_time's and one of complx_rating for
    the selected games
    '''

    time       = []
    complexity = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:
                
                curs.execute("""SELECT play_time, complx_rating 
                                FROM boardgames
                                WHERE play_time < %s AND complx_rating < %s;
                             """,(time_cutoff, cmplx_cutoff))

            except:

                print "Failed to SELECT from table"

                return None,None

            for row_tuple in curs.fetchall():

                time.append(row_tuple[0])

                complexity.append(row_tuple[1])

    return time, complexity

def popular_designer_for_mechanism():
    pass

def avg_rating_per_mechanic():
    
    mechanic_list   = list_of_unique_items('mechanics')

    avg_rating_list = []

    num_games_list  = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            for mechanic in mechanic_list:

                try:
                    
                    curs.execute("""SELECT AVG(boardgames.geek_rating)
                                    FROM mechanics 
                                    INNER JOIN boardgames 
                                    ON boardgames.id=mechanics.bg_id 
                                    WHERE mechanics.mechanic = %s;
                                 """, (mechanic,))

                except:

                    print "Failed to SELECT from table"

                    return

                avg_rating_list.append(curs.fetchone()[0])

                try:
                    
                    curs.execute("""SELECT COUNT(bg_id)
                                    FROM mechanics  
                                    WHERE mechanic = %s;
                                 """, (mechanic,))

                except:

                    print "Failed to SELECT from table"

                    return

                num_games_list.append(int(curs.fetchone()[0]))

    return mechanic_list, avg_rating_list, num_games_list

def avg_rating_per_mechanic_for_rank(rank=10000):
    
    mechanic_list   = list_of_unique_items_for_rank('mechanics', rank)

    avg_rating_list = []

    num_games_list  = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            for mechanic in mechanic_list:

                try:
                    
                    curs.execute("""SELECT AVG(boardgames.geek_rating)
                                    FROM mechanics 
                                    INNER JOIN boardgames 
                                    ON boardgames.id=mechanics.bg_id 
                                    WHERE mechanics.mechanic = %s
                                    AND boardgames.rank < %s;
                                 """, (mechanic, rank))

                except:

                    print "Failed to SELECT from table"

                    return

                avg_rating_list.append(curs.fetchone()[0])

                try:
                    
                    curs.execute("""SELECT COUNT(bg_id)
                                    FROM mechanics  
                                    INNER JOIN boardgames 
                                    ON boardgames.id=mechanics.bg_id 
                                    WHERE mechanics.mechanic = %s
                                    AND boardgames.rank < %s;
                                 """, (mechanic, rank))

                except:

                    print "Failed to SELECT from table"

                    return

                num_games_list.append(int(curs.fetchone()[0]))

    return mechanic_list, avg_rating_list, num_games_list

def scatter_plot_all_mechanics(top=3):

    fig, ax = plt.subplots(1,1)
    
    mech_list, avg_list, num_list = avg_rating_per_mechanic()

    avg_copy = np.copy(avg_list)
    avg_copy.sort() # Used for finding top 3 average rated mechanic

    num_copy = np.copy(num_list)
    num_copy.sort() # Used for finding top 3 most frequent mechanic
    
    for label, x, y, n in zip(mech_list, xrange(len(mech_list)), avg_list,
                                                                 num_list):
        
        # Label the top 3 for number of mechanics and for average rating
        if y >= avg_copy[-top]:

            plt.scatter(x, y, s=n, alpha=0.9, c=colors[1],
                        label=label)

            plt.scatter(x, y, s=15, c='k')

            plt.annotate(label, xy = (x, y))

        elif n >= num_copy[-top]:

            plt.scatter(x, y, s=n, alpha=0.9, c=colors[2],
                        label=label)

            plt.scatter(x, y, s=15, c='k')

            plt.annotate(label, xy = (x, y))

        else:

            plt.scatter(x, y, s=10, c='k')

            plt.scatter(x, y, s=n, alpha=0.5, c=colors[0],
                        label=label)

    ax.set_ylabel('Average Geek Rating')

    ax.xaxis.set_visible(False)

    ax.set_title("Game Mechanics' Influence on All Boardgames")

    plt.show()

def scatter_plot_mechanics_with_rank(rank, top=3):

    fig, ax = plt.subplots(1,1)
    
    mech_list, avg_list, num_list = avg_rating_per_mechanic_for_rank(rank)
    
    avg_copy = np.copy(avg_list)
    avg_copy.sort() # Used for finding top 3 average rated mechanic

    num_copy = np.copy(num_list)
    num_copy.sort() # Used for finding top 3 most frequent mechanic

    for label, x, y, n in zip(mech_list, xrange(len(mech_list)),avg_list,
                                                                num_list):
        
        # Label the top 3 for number of mechanics and for average rating

        if y >= avg_copy[-top]:

            plt.scatter(x, y, s=n*np.max(num_list)*100/rank, alpha=0.9, c=colors[1],
                        label=label)

            plt.scatter(x, y, s=15, c='k')

            plt.annotate(label, xy = (x, y))

        elif n >= num_copy[-top]:

            plt.scatter(x, y, s=n*np.max(num_list)*100/rank, alpha=0.9, c=colors[2],
                        label=label)

            plt.scatter(x, y, s=15, c='k')

            plt.annotate(label, xy = (x, y))

        else:

            plt.scatter(x, y, s=10, c='k')

            plt.scatter(x, y, s=n*np.max(num_list)*100/rank, alpha=0.5, c=colors[0],
                        label=label)

    ax.set_ylabel('Average Geek Rating')

    ax.xaxis.set_visible(False)

    ax.set_title("Game Mechanics' Influence on Top "+str(rank)+\
                 ' Boardgames')

    plt.show()
