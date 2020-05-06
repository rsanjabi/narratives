from abc import ABC, abstractmethod
# from typing import List
# import csv
import os
import sys

# import logging
# from logging import Logger
# from pathlib import Path
import psycopg2
# from psycopg2 import connect, sql

import config as cfg
# import utils.paths as paths
# from scrape.progress import Progress


print(os.environ['HOME'])


class AO3DB(ABC):

    def __init__(self, fandom: str):
        self.fandom = fandom
        self.cursor, self.connect = self.open()
        # check for existence of tables, creating if necessary

    def open(self):
        ''' Open database connection. Returns cursor and connection '''
        try:
            print("Opening connection...")
            connect = psycopg2.connect(
                            host=cfg.HOST,
                            database=os.environ['DB_NAME'],
                            user=os.environ['DB_USER'],
                            password=os.environ['DB_PASS'],
            )
            cur = connect.cursor()

            # Set search path to look for 'one_most_recent' schema
            # cur.execute("SET search_path TO one_most_recent,public;")
            # connect.commit()

            print(f"SUCCESS")

        except Exception as e:
            print("There was an error connecting to the database: ", e)
            sys.exit()

        return cur, connect

    def close(self):
        self.cursor.close()
        self.connect.close()
        print(f"Connection closed.")

    @abstractmethod
    def insert_from_csv(self):
        pass

    @abstractmethod
    def insert_str(self):
        pass

    @abstractmethod
    def table_creation(self):
        pass


"""
def insert_ein(cur, connect, ein):
    ''' Given an EIN number checks to see if it's in the
        aka_dba table and adds it if needed. '''

    query = "SELECT ein FROM aka_dba WHERE ein = '{}'".format(ein)
    cur.execute(query)
    results = cur.fetchall()
    if len(results) == 0:
        print(f"Adding new ein to aka_dba.")
        insert_query = "insert into aka_dba (ein) values ("+ein+");"
        cur.execute(insert_query, results)
        connect.commit()
    return

def find_records(cur, connect, search):
    ''' Generates rows given a search query.
        Returns dict: ein, name, website '''

    cur.execute(search)
    records = cur.fetchall()
    org = {}
    for row in records:
        org['ein'] = row[0]
        org['name'] = row[1]
        org['website'] = row[2]
        print(org['ein']+" ", end='')
        yield org
    return

def aka_table_creation(cur, connect):
    ''' Check for aka_dba table existence, create and add columns as needed.'''

    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables \
                WHERE table_schema = %s AND \
                table_name = %s );",
                ('one_most_recent', 'aka_dba'))

    # Create Table if it doesn't exist
    if (cur.fetchone()[0] != True):
        cur.execute("CREATE TABLE aka_dba (ein text UNIQUE PRIMARY KEY)")
        connect.commit()

    # Check to see if column cselico_website_liaka exists
    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.columns \
        WHERE table_schema = %s AND table_name = %s AND column_name= %s );",
        ('one_most_recent', 'aka_dba', 'cselico_website_liaka'))
    # Create if not already there
    if (cur.fetchone()[0] != True):
        cur.execute("ALTER TABLE aka_dba"
                    " ADD COLUMN cselico_website_liaka text")
        connect.commit()

    # Check to see if column 'cselico_website_liurl exists
    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.columns \
            WHERE table_schema = %s AND \
            table_name = %s AND column_name= %s );",
            ('one_most_recent', 'aka_dba','cselico_website_liurl'))
    # Create if not already there
    if (cur.fetchone()[0] != True):
        cur.execute("ALTER TABLE aka_dba ADD "
                    "COLUMN cselico_website_liurl text")
        connect.commit()

    # Check to see if column 'binglico_orgname_liaka exists
    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.columns \
            WHERE table_schema = %s AND \
            table_name = %s AND column_name= %s );",
            ('one_most_recent', 'aka_dba','binglico_orgname_liaka'))
    # Create if not already there
    if (cur.fetchone()[0] != True):
        cur.execute("ALTER TABLE aka_dba ADD "
                    "COLUMN binglico_orgname_liaka text")
        connect.commit()

    # Check to see if column 'binglico_orgname_liurl exists
    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.columns \
            WHERE table_schema = %s AND \
            table_name = %s AND column_name= %s );",
            ('one_most_recent', 'aka_dba','binglico_orgname_liurl'))
    # Create if not already there
    if (cur.fetchone()[0] != True):
        cur.execute("ALTER TABLE aka_dba ADD COLUMN \
                    "binglico_orgname_liurl text")
        connect.commit()

       # Check to see if column 'binglico_orgname_liaka exists
    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.columns \
            WHERE table_schema = %s AND \
            table_name = %s AND column_name= %s );",
            ('one_most_recent', 'aka_dba','csekg_orgname_kgaka'))
    # Create if not already there
    if (cur.fetchone()[0] != True):
        cur.execute("ALTER TABLE aka_dba ADD COLUMN csekg_orgname_kgaka text")
        connect.commit()

    # Check to see if column 'binglico_orgname_liurl exists
    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.columns \
            WHERE table_schema = %s AND t\
            able_name = %s AND column_name= %s );",
            ('one_most_recent', 'aka_dba','csekg_orgname_kgurl'))
    # Create if not already there
    if (cur.fetchone()[0] != True):
        cur.execute("ALTER TABLE aka_dba ADD COLUMN csekg_orgname_kgurl text")
        connect.commit()

    return


if __name__ == "__main__":

    cur, connect = open_db()
    aka_table_creation(cur, connect)
    rows = find_records(cur, connect, config.SELECT)
    print("Searching for akas and dbas. This might take awhile.")
    bar = progressbar.ProgressBar(redirect_stdout=True, max_value=config.LIMIT)

    for count, row in enumerate(rows, start=1):
        bar.update(count)
        insert_ein(cur, connect, row['ein'])
        searches.cselico_website_search(cur, connect, row,
                                        search_scope=config.SCOPE)
        searches.binglico_orgname_search(cur, connect, row, driver,
                                         search_scope=config.SCOPE)
        searches.csekg_orgname_search(cur, connect, row,
                                      search_scope=config.SCOPE)
        print("")
        if count >= config.LIMIT:
            break

    print("Searches complete.")
    print("Writing results to", config.FILENAME+".json")
    export_to_json(cur, config.FILENAME)
"""
