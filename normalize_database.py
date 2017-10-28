'''
Since 6 columns in the boardgames table contain text arrays,
it makes it significantly more difficult to query based on those
columns. Therefore this script normalizes the database by creating
separate tables for those 6 columns.
'''

import psycopg2
from bg_scraper import DATABASE # Global Variable

def create_designers_table():

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:
            try:
                
                curs.execute("""CREATE TABLE designers (designer text,
                                                        bg_id     int);""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to create new designers table"

                return

            try:
                
                curs.execute("""SELECT designers, id FROM boardgames;""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to select designers,id from boardgames"

                return

            for row_tuple in curs.fetchall():

                designer_list, bg_id = row_tuple

                for designer in designer_list:

                    curs.execute("""INSERT INTO designers (designer, bg_id)
                                      VALUES (%s, %s);""", (designer, bg_id))

def create_artists_table():

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:
            try:
                
                curs.execute("""CREATE TABLE artists (artist text,
                                                      bg_id   int);""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to create new artists table"

                return

            try:
                
                curs.execute("""SELECT artists, id FROM boardgames;""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to select artists,id from boardgames"

                return

            for row_tuple in curs.fetchall():

                artist_list, bg_id = row_tuple

                for artist in artist_list:

                    curs.execute("""INSERT INTO artists (artist, bg_id)
                                      VALUES (%s, %s);""", (artist, bg_id))

def create_categories_table():

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:
            try:
                
                curs.execute("""CREATE TABLE categories (category text,
                                                         bg_id     int);""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to create new categories table"

                return

            try:
                
                curs.execute("""SELECT categories, id FROM boardgames;""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to select categories,id from boardgames"

                return

            for row_tuple in curs.fetchall():

                category_list, bg_id = row_tuple

                for category in category_list:

                    curs.execute("""INSERT INTO categories (category, bg_id)
                                      VALUES (%s, %s);""", (category, bg_id))

def create_mechanics_table():

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:
            try:
                
                curs.execute("""CREATE TABLE mechanics (mechanic text,
                                                        bg_id     int);""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to create new mechanics table"

                return

            try:
                
                curs.execute("""SELECT mechanics, id FROM boardgames;""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to select mechanics,id from boardgames"

                return

            for row_tuple in curs.fetchall():

                mechanic_list, bg_id = row_tuple

                for mechanic in mechanic_list:

                    curs.execute("""INSERT INTO mechanics (mechanic, bg_id)
                                      VALUES (%s, %s);""", (mechanic, bg_id))

def create_families_table():

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:
            try:
                
                curs.execute("""CREATE TABLE families (family text,
                                                       bg_id   int);""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to create new families table"

                return

            try:
                
                curs.execute("""SELECT family, id FROM boardgames;""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to select family,id from boardgames"

                return

            for row_tuple in curs.fetchall():

                family_list, bg_id = row_tuple

                for family in family_list:

                    curs.execute("""INSERT INTO families (family, bg_id)
                                      VALUES (%s, %s);""", (family, bg_id))

def create_types_table():

    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as curs:
            try:
                
                curs.execute("""CREATE TABLE types (type text,
                                                    bg_id int);""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to create new types table"

                return

            try:
                
                curs.execute("""SELECT type, id FROM boardgames;""")

            except:

                curs.execute("""ROLLBACK;""")

                print "Failed to select type,id from boardgames"

                return

            for row_tuple in curs.fetchall():

                type_list, bg_id = row_tuple

                for bg_type in type_list:

                    curs.execute("""INSERT INTO types (type, bg_id)
                                      VALUES (%s, %s);""", (bg_type, bg_id))

if __name__ ==  "__main__":

    create_designers_table()
    create_artists_table()
    create_categories_table()
    create_mechanics_table()
    create_families_table()
    create_types_table()
