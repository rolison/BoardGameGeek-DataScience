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
    Same as list_of_unique_items() but can filter results for games that
    are above a certain rank.

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

    Returns a list of lists, each sublist containing the unique item name
    and the number of gaems associated with it.
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

def avg_geek_rating_playtime_per_mechanic(rank=10000, sortby=None):
    '''
    Same exact capabilities as avg_rating_per_mechanic() but it only
    considers games that are above a specified rank on boardgamegeek.com.

    Returns a list of the unique mechanics, a list of the average geek rating 
    for the games associated with those mechanics, and a list of the number of
    games associated with those mechanics; All for games above a specified rank.
    '''
    if sortby is not None:
        if sortby is 'num':
            sortby = 'ORDER BY COUNT(boardgames.id) DESC;'

        elif sortby is 'geek':
            sortby = 'ORDER BY AVG(boardgames.geek_rating) DESC;'

        elif sortby is 'playtime':
            sortby = 'ORDER BY AVG(boardgames.play_time) DESC;'

        else:

            print "Requested sortby is not an option. Options include:"
            print "num, geek, playtime"
            return

    else:
        sortby = ';'

    mechanic     = []

    avg_rating   = []

    avg_playtime = []

    num_games    = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:

                curs.execute("""SELECT mechanics.mechanic, 
                                       AVG(boardgames.geek_rating),
                                       AVG(boardgames.play_time),
                                       COUNT(boardgames.id)
                                FROM mechanics
                                INNER JOIN boardgames
                                ON boardgames.id=mechanics.bg_id
                                WHERE boardgames.rank < %s
                                GROUP BY mechanics.mechanic
                            """ + sortby, (rank,))

            except:

                print "Failed to SELECT from table"

                return

            for row_tuple in curs.fetchall():

                mechanic.append(row_tuple[0])

                avg_rating.append(row_tuple[1])

                avg_playtime.append(row_tuple[2])

                num_games.append(int(row_tuple[3]))

    return mechanic, avg_rating, avg_playtime, num_games

def geek_rating_avg_rating_for_item_in_column(column, item_name):
    '''
    Grab the geek_rating and avg_rating from boardgames table
    for a specified column and a specified item in that column

    Returns a list of geek ratings and a list of average ratings
    from the boardgames table. 
    '''

    sql_dict = {'designers' :"""SELECT boardgames.geek_rating, 
                                       boardgames.avg_rating
                                FROM designers 
                                INNER JOIN boardgames 
                                ON boardgames.id=designers.bg_id 
                                WHERE designers.designer = %s;
                             """,
                'artists'   :"""SELECT boardgames.geek_rating, 
                                       boardgames.avg_rating
                                FROM artists 
                                INNER JOIN boardgames 
                                ON boardgames.id=artists.bg_id 
                                WHERE artists.artist = %s;
                             """, 
                'categories':"""SELECT boardgames.geek_rating, 
                                       boardgames.avg_rating
                                FROM categories 
                                INNER JOIN boardgames 
                                ON boardgames.id=categories.bg_id 
                                WHERE categories.category = %s;
                             """, 
                'mechanics' :"""SELECT boardgames.geek_rating, 
                                       boardgames.avg_rating
                                FROM mechanics 
                                INNER JOIN boardgames 
                                ON boardgames.id=mechanics.bg_id 
                                WHERE mechanics.mechanic = %s;
                             """,
                'family'    :"""SELECT boardgames.geek_rating, 
                                       boardgames.avg_rating
                                FROM families 
                                INNER JOIN boardgames 
                                ON boardgames.id=families.bg_id 
                                WHERE families.family = %s;
                             """, 
                'type'      :"""SELECT boardgames.geek_rating, 
                                       boardgames.avg_rating
                                FROM types 
                                INNER JOIN boardgames 
                                ON boardgames.id=types.bg_id 
                                WHERE types.type = %s;
                             """}

    if column not in sql_dict.keys():

        print "\nRequested column does not exist in table."
        print "Options for column:", sql_dict.keys()

        return

    geek_r = []
    avg_r  = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:
                
                curs.execute(sql_dict[column], (item_name,))

            except:

                print "Failed to SELECT from table"

                return

            for row_tuple in curs.fetchall():
                    
                geek_r.append(row_tuple[0])

                avg_r.append(row_tuple[1])
    
    return geek_r, avg_r

def num_voters_for_item_in_column(column, item_name, voter_threshold):
    '''
    Grab the num_voters from boardgames table
    for a specified column and a specified item in that column.
    Can filter the games selected by specifying how many voters there must
    be associated with a game (num_voters column)

    Returns a list of number of voters from the boardgames table.
    '''

    sql_dict = {'designers' :"""SELECT boardgames.num_voters
                                FROM designers 
                                INNER JOIN boardgames 
                                ON boardgames.id=designers.bg_id 
                                WHERE designers.designer = %s
                                AND boardgames.num_voters > %s;
                             """,
                'artists'   :"""SELECT boardgames.num_voters
                                FROM artists 
                                INNER JOIN boardgames 
                                ON boardgames.id=artists.bg_id 
                                WHERE artists.artist = %s
                                AND boardgames.num_voters > %s;
                             """, 
                'categories':"""SELECT boardgames.num_voters
                                FROM categories 
                                INNER JOIN boardgames 
                                ON boardgames.id=categories.bg_id 
                                WHERE categories.category = %s
                                AND boardgames.num_voters > %s;
                             """, 
                'mechanics' :"""SELECT boardgames.num_voters
                                FROM mechanics 
                                INNER JOIN boardgames 
                                ON boardgames.id=mechanics.bg_id 
                                WHERE mechanics.mechanic = %s
                                AND boardgames.num_voters > %s;
                             """,
                'family'    :"""SELECT boardgames.num_voters
                                FROM families 
                                INNER JOIN boardgames 
                                ON boardgames.id=families.bg_id 
                                WHERE families.family = %s
                                AND boardgames.num_voters > %s;
                             """, 
                'type'      :"""SELECT boardgames.num_voters
                                FROM types 
                                INNER JOIN boardgames 
                                ON boardgames.id=types.bg_id 
                                WHERE types.type = %s
                                AND boardgames.num_voters > %s;
                             """}

    if column not in sql_dict.keys():

        print "\nRequested column does not exist in table."
        print "Options for column:", sql_dict.keys()

        return

    num_voters = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:
                
                curs.execute(sql_dict[column], (item_name, voter_threshold))

            except:

                print "Failed to SELECT from table"

                return

            for row_tuple in curs.fetchall():
                    
                num_voters.append(int(row_tuple[0]))
    
    return num_voters

def geek_rating_comp_rating_for_item_in_column(column, item_name, num_voters):
    '''
    Grab the geek_rating and complx_rating from boardgames table
    for a specified column and a specified item in that column.
    Can filter the games selected by specifying how many voters there must
    be associated with a game (num_voters column)

    Returns a list of geek ratings and a list of complexity ratings
    from the boardgames table. 
    '''

    sql_dict = {'designers' :"""SELECT boardgames.geek_rating, 
                                       boardgames.complx_rating
                                FROM designers 
                                INNER JOIN boardgames 
                                ON boardgames.id=designers.bg_id 
                                WHERE designers.designer = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.num_voters > %s;
                             """,
                'artists'   :"""SELECT boardgames.geek_rating, 
                                       boardgames.complx_rating
                                FROM artists 
                                INNER JOIN boardgames 
                                ON boardgames.id=artists.bg_id 
                                WHERE artists.artist = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.num_voters > %s;
                             """, 
                'categories':"""SELECT boardgames.geek_rating, 
                                       boardgames.complx_rating
                                FROM categories 
                                INNER JOIN boardgames 
                                ON boardgames.id=categories.bg_id 
                                WHERE categories.category = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.num_voters > %s;
                             """, 
                'mechanics' :"""SELECT boardgames.geek_rating, 
                                       boardgames.complx_rating
                                FROM mechanics 
                                INNER JOIN boardgames 
                                ON boardgames.id=mechanics.bg_id 
                                WHERE mechanics.mechanic = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.num_voters > %s;
                             """,
                'family'    :"""SELECT boardgames.geek_rating, 
                                       boardgames.complx_rating
                                FROM families 
                                INNER JOIN boardgames 
                                ON boardgames.id=families.bg_id 
                                WHERE families.family = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.num_voters > %s;
                             """, 
                'type'      :"""SELECT boardgames.geek_rating, 
                                       boardgames.complx_rating
                                FROM types 
                                INNER JOIN boardgames 
                                ON boardgames.id=types.bg_id 
                                WHERE types.type = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.num_voters > %s;
                             """}

    if column not in sql_dict.keys():

        print "\nRequested column does not exist in table."
        print "Options for column:", sql_dict.keys()

        return

    geek_r = []
    comp_r  = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:
                
                curs.execute(sql_dict[column], (item_name,num_voters))

            except:

                print "Failed to SELECT from table"

                return

            for row_tuple in curs.fetchall():
                    
                geek_r.append(row_tuple[0])

                comp_r.append(row_tuple[1])
    
    return geek_r, comp_r

def comp_rating_sugg_age_for_item_in_column(column, item_name, num_voters):
    '''
    Grab the complx_rating and sugg_age from boardgames table
    for a specified column and a specified item in that column.
    Can filter the games selected by specifying how many voters there must
    be associated with a game (num_voters column)

    Returns a list of complexity ratings and a list of suggested ages
    from the boardgames table.
    '''

    sql_dict = {'designers' :"""SELECT boardgames.complx_rating, 
                                       boardgames.sugg_age
                                FROM designers 
                                INNER JOIN boardgames 
                                ON boardgames.id=designers.bg_id 
                                WHERE designers.designer = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.sugg_age > 0
                                AND boardgames.num_voters > %s;
                             """,
                'artists'   :"""SELECT boardgames.complx_rating, 
                                       boardgames.sugg_age
                                FROM artists 
                                INNER JOIN boardgames 
                                ON boardgames.id=artists.bg_id 
                                WHERE artists.artist = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.sugg_age > 0
                                AND boardgames.num_voters > %s;
                             """, 
                'categories':"""SELECT boardgames.complx_rating, 
                                       boardgames.sugg_age
                                FROM categories 
                                INNER JOIN boardgames 
                                ON boardgames.id=categories.bg_id 
                                WHERE categories.category = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.sugg_age > 0
                                AND boardgames.num_voters > %s;
                             """, 
                'mechanics' :"""SELECT boardgames.complx_rating, 
                                       boardgames.sugg_age
                                FROM mechanics 
                                INNER JOIN boardgames 
                                ON boardgames.id=mechanics.bg_id 
                                WHERE mechanics.mechanic = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.sugg_age > 0
                                AND boardgames.num_voters > %s;
                             """,
                'family'    :"""SELECT boardgames.complx_rating, 
                                       boardgames.sugg_age
                                FROM families 
                                INNER JOIN boardgames 
                                ON boardgames.id=families.bg_id 
                                WHERE families.family = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.sugg_age > 0
                                AND boardgames.num_voters > %s;
                             """, 
                'type'      :"""SELECT boardgames.complx_rating, 
                                       boardgames.sugg_age
                                FROM types 
                                INNER JOIN boardgames 
                                ON boardgames.id=types.bg_id 
                                WHERE types.type = %s
                                AND boardgames.complx_rating > 0
                                AND boardgames.sugg_age > 0
                                AND boardgames.num_voters > %s;
                             """}

    if column not in sql_dict.keys():

        print "\nRequested column does not exist in table."
        print "Options for column:", sql_dict.keys()

        return

    comp_r  = []
    sugg_a  = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:
                
                curs.execute(sql_dict[column], (item_name,num_voters))

            except:

                print "Failed to SELECT from table"

                return

            for row_tuple in curs.fetchall():

                comp_r.append(row_tuple[0])

                sugg_a.append(row_tuple[1])
    
    return comp_r, sugg_a

# =============================================================================
#  Start of Plotting Functions
# =============================================================================

def scatter_plot_mechanics_with_rank(rank, top=3):

    fig, ax = plt.subplots(1,1)

    fig.set_size_inches(11,8)

    ax.set_ylabel('Average Geek Rating')

    ax.set_xlabel('Average Playtime (minutes)')

    if rank >= 10000:
        ax.set_title("Game Mechanics' Influence on All Boardgames")

    else:
        ax.set_title("Game Mechanics' Influence on Top "+str(rank)+\
                     ' Boardgames')

    # First plot all data =====================================================
    
    mech_list, avg_list, play_list, num_list = \
                   avg_geek_rating_playtime_per_mechanic(rank)

    sizes = __scale_size(num_list)

    plt.scatter(play_list, avg_list, s=sizes, alpha=0.75)

    # Next plot top number games ==============================================

    mech_list, avg_list, play_list, num_sorted = \
                    avg_geek_rating_playtime_per_mechanic(rank, sortby='num')

    sizes = __scale_size(num_sorted)

    plt.scatter(play_list[:top], avg_list[:top], s=sizes[:top], alpha=0.5,
                   label='Top ' + str(top)+ ' Number of Games with Mechanic')

    for label, x, y in zip(mech_list[:top], play_list[:top], avg_list[:top]):
        plt.scatter(x, y, s=10, c='k')
        plt.annotate(label, xy = (x, y))

    # Next plot top geek ratings ==============================================

    mech_list, avg_sorted, play_list, num_list = \
                    avg_geek_rating_playtime_per_mechanic(rank, sortby='geek')

    sizes = __scale_size(num_list)

    plt.scatter(play_list[:top], avg_sorted[:top], s=sizes[:top], alpha=1,
                   label='Top ' + str(top)+ ' Geek Ratings')

    for label, x, y in zip(mech_list[:top], play_list[:top], avg_sorted[:top]):
        plt.scatter(x, y, s=10, c='k')
        plt.annotate(label, xy = (x, y))

    # Next plot top playtimes =================================================

    mech_list, avg_list, play_sorted, num_list = \
                 avg_geek_rating_playtime_per_mechanic(rank, sortby='playtime')

    sizes = __scale_size(num_list)

    plt.scatter(play_sorted[:top], avg_list[:top], s=sizes[:top], alpha=1,
                   label='Top ' + str(top)+ ' Average Playtimes')

    for label, x, y in zip(mech_list[:top], play_sorted[:top], avg_list[:top]):
        plt.scatter(x, y, s=10, c='k')
        plt.annotate(label, xy = (x, y))

    ax.legend()

    plt.show()

def scatter_plot_geekr_vs_avgr_for_column(column, item_subset=None):
    '''
    Creates a scatter plot for a given column from the boardgames table.

    Y-axis will be the Geek Rating; X-axis the Average Rating

    column examples: mechanics, categories, type
    '''

    fig, ax = plt.subplots(1,1)

    col_data = count_column(column)

    for item_name, game_count in col_data:

        # If you only want to plot a few items from the full list
        if item_subset is not None:
            if item_name in item_subset:

                geekr, avgr = geek_rating_avg_rating_for_item_in_column(column,
                                                                     item_name)

                num_v = num_voters_for_item_in_column(column, item_name)

                avg_num_v = int(np.mean(num_v).round())

                plt.scatter(avgr, geekr, alpha=0.3,
                            label=str(game_count)+' '+item_name \
                            +' \nAverage Num Voters: ' + str(avg_num_v))

        else:

            geekr, avgr = geek_rating_avg_rating_for_item_in_column(column,
                                                                item_name)

            num_v = num_voters_for_item_in_column(column, item_name)

            avg_num_v = int(np.mean(num_v).round())

            plt.scatter(avgr, geekr, alpha=0.3,
                        label=str(game_count)+' '+item_name \
                        +' \nAverage Num Voters: ' + str(avg_num_v))

    plt.plot(np.linspace(5.5, 9.5), np.linspace(5.5,9.5), c='k', lw=2, 
             label='Geek Rating = Average Rating')

    ax.legend()

    ax.set_ylabel('Geek Rating')

    ax.set_xlabel('Average Rating')

    ax.set_title(column.capitalize())

    plt.show()

def scatter_plot_diffr_vs_num_voters():

    avg_geekr = []
    avg_avg_r = []
    num_v = []

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:

            try:
                
                curs.execute("""SELECT num_voters, 
                                       AVG(geek_rating),
                                       AVG(avg_rating)
                                FROM boardgames
                                GROUP BY num_voters
                                ORDER BY num_voters ASC;""")

            except:

                print "Failed to SELECT from table"

                return

            for row_tuple in curs.fetchall():
                
                num_v.append(int(row_tuple[0]))
                avg_geekr.append(row_tuple[1])
                avg_avg_r.append(row_tuple[2])
    #return num_v, avg_geekr, avg_avg_r
    diff = [a-g for a,g in zip(avg_avg_r, avg_geekr)]

    fig, ax = plt.subplots(1,1)

    plt.plot(num_v, diff)#, alpha=0.5)

    ax.set_ylabel('Average Rating - Geek Rating')

    ax.set_xlabel('Number of Voters')

    ax.set_title("Geek Rating vs Number of Voters")

    plt.show()

def scatter_plot_geekr_vs_complxr(column, item_subset=None, num_voters=1000):
    '''
    Creates a scatter plot for a given column from the boardgames table.

    Y-axis will be the Geek Rating; X-axis the Complexity Rating

    column examples: mechanics, categories, type
    '''

    fig, ax = plt.subplots(1,1)

    col_data = count_column(column)

    for item_name, game_count in col_data:

        # If you only want to plot a few items from the full list
        if item_subset is not None:
            if item_name in item_subset:

                geekr, compr = geek_rating_comp_rating_for_item_in_column(column,
                                                                       item_name, 
                                                                      num_voters)

                num_v = num_voters_for_item_in_column(column, item_name, num_voters)

                avg_num_v = int(np.mean(num_v).round())

                plt.scatter(compr, geekr, alpha=0.75,
                            label=str(game_count)+' '+item_name \
                            +' \nAverage Num Voters: ' + str(avg_num_v))

        else:

            geekr, compr = geek_rating_comp_rating_for_item_in_column(column,
                                                                   item_name,
                                                                  num_voters)

            num_v = num_voters_for_item_in_column(column, item_name, num_voters)

            avg_num_v = int(np.mean(num_v).round())

            plt.scatter(compr, geekr, alpha=0.75,
                        label=str(game_count)+' '+item_name \
                        +' \nAverage Num Voters: ' + str(avg_num_v))

    #plt.plot(np.linspace(5.5, 9.5), np.linspace(5.5,9.5), c='k', lw=2, 
    #         label='Geek Rating = Average Rating')

    ax.legend()

    ax.set_ylabel('Geek Rating')

    ax.set_xlabel('Complexity Rating')

    ax.set_title(column.capitalize() + " In Games With More Than "+\
                 str(num_voters) + " Voters")

    plt.show()

def scatter_plot_complxr_vs_sugg_age(column, item_subset=None, num_voters=0):
    '''
    Creates a scatter plot for a given column from the boardgames table.

    Y-axis will be the Geek Rating; X-axis the Complexity Rating

    column examples: mechanics, categories, type
    '''

    fig, ax = plt.subplots(1,1)

    col_data = count_column(column)

    for item_name, game_count in col_data:

        # If you only want to plot a few items from the full list
        if item_subset is not None:
            if item_name in item_subset:

                compr, sugg_age = comp_rating_sugg_age_for_item_in_column(column,
                                                                       item_name, 
                                                                      num_voters)

                num_v = num_voters_for_item_in_column(column, item_name, num_voters)

                avg_num_v = int(np.mean(num_v).round())

                plt.scatter(sugg_age, compr, alpha=0.75,
                            label=item_name)# \
                            #+' \nAverage Num Voters: ' + str(avg_num_v))
                            #label=str(game_count)+' '+item_name \
                            #+' \nAverage Num Voters: ' + str(avg_num_v))

        else:

            compr, sugg_age = comp_rating_sugg_age_for_item_in_column(column,
                                                                   item_name,
                                                                  num_voters)

            num_v = num_voters_for_item_in_column(column, item_name, num_voters)

            avg_num_v = int(np.mean(num_v).round())

            plt.scatter(sugg_age, compr, alpha=0.75,
                        label=item_name)# \
                         #   +' \nAverage Num Voters: ' + str(avg_num_v))
                        #label=str(game_count)+' '+item_name \
                        #+' \nAverage Num Voters: ' + str(avg_num_v))

    #plt.plot(np.linspace(5.5, 9.5), np.linspace(5.5,9.5), c='k', lw=2, 
    #         label='Geek Rating = Average Rating')

    ax.legend()

    ax.set_ylabel('Complexity Rating')

    ax.set_xlabel('Suggested Age')

    ax.set_title(column.capitalize() + " In Games")# With More Than "+\
                 #str(num_voters) + " Voters")

    plt.show()

def __scale_size(val_list, min=25, max=1000):
    '''
    Helper function to maintain scale of the circle sizes in scatter plots
    '''
    
    return [float(val - np.min(val_list))/
            (np.max(val_list) - np.min(val_list))*(max-min) + min \
            for val in val_list]


