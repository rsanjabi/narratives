import os
import sys
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame
import logging
from logging import Logger
from pathlib import Path
import psycopg2
import config as cfg


class AO3DB():

    def __init__(self, log_name: str, log_path: Path, logger=None):
        self.log_name = log_name
        self.log_path = log_path
        self.cursor, self.connect = self.open()
        if logger is not None:
            self.logger = logger
        else:
            self.logger = self._init_log()

    def open(self):
        ''' Open database connection. Returns cursor and connection '''
        try:
            connect = psycopg2.connect(
                            host=cfg.HOST,
                            database=os.environ['DB_NAME'],
                            user=os.environ['DB_USER'],
                            password=os.environ['DB_PASS'],
            )
            cur = connect.cursor()
        except Exception as e:
            print("There was an error connecting to the database: ", e)
            sys.exit()

        return cur, connect

    def close(self):
        self.cursor.close()
        self.connect.close()
        print("Connection closed.")

    def _init_log(self) -> Logger:
        logger = logging.getLogger(self.log_name)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(self.log_path, mode='a')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info("********************************")
        return logger

    def fanwork_exists(self, work_id: str) -> bool:
        cur = self.connect.cursor()
        sql = "SELECT EXISTS (SELECT 1 FROM staging_meta WHERE work_id = %s);"
        cur.execute(sql, (work_id,))
        return cur.fetchone()[0]

    def fanwork_select(self, work_id: str) -> str:
        cur = self.connect.cursor()
        sql = "SELECT * FROM staging_meta WHERE work_id = %s;"
        cur.execute(sql, (work_id,))
        return cur.fetchone()

    def kudo_matrix(self) -> DataFrame:
        # Kudos to dataframe
        sql = """
              SELECT work_id, kudo_givers
              FROM staging_meta
              WHERE kudo_givers is not Null
              AND 'Star Wars:Rebels' = ANY(fandom);
              """
        sql2 = """
              SELECT work_id, kudo_givers
              FROM staging_meta
              WHERE kudo_givers is not Null
              AND ('Star Wars: The Clone Wars (2008) - All Media Types' = ANY(fandom)
              OR 'Star Wars Prequel Trilogy' = ANY (fandom)
              OR 'Star Wars: Rebellion Era - All Media Types' = ANY(fandom)
                OR 'Star Wars: Rebels' = ANY(fandom)
                OR 'Star Wars: Ahsoka - E. K. Johnston'  = ANY(fandom)
                OR 'Rogue One: A Star Wars Story (2016)'  = ANY(fandom)
                );
              """
        data = pd.read_sql_query(sql2, self.connect)
        df = data.explode('kudo_givers')
        return df

    def kudo_scrape_date(self, work_id: str) -> datetime:
        cur = self.connect.cursor()
        sql = "select kudo_scr_date from staging_meta where work_id = %s ;"
        cur.execute(sql, (work_id,))
        return cur.fetchone()[0]

    def missing_kudos(self, batch_size: str):
        sql = """
                SELECT work_id FROM staging_meta
                WHERE kudo_scr_date is null
                ORDER BY random()
                LIMIT %s;
            """
        cur = self.connect.cursor()
        cur.execute(sql, (int(batch_size),))
        for _ in range(int(batch_size)):
            yield cur.fetchone()[0]

    def _recently_updated(self, work_id: str) -> bool:
        scr_date = self.kudo_scrape_date(work_id)
        if scr_date is None:
            return False
        return (scr_date > (datetime.now()-timedelta(cfg.SCR_WINDOW)))
