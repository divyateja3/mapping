import os
import time
import sqlalchemy
import psycopg2
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import text

class Connection:

    def __init__(self):
        load_dotenv()
        engine = sqlalchemy.create_engine(os.getenv('CONNECTION_STRING'))

        try:
            self.connection = engine.connect()
            print("Connected to server : SUCCESS")
        except SQLAlchemyError as error:
            raise f'[CONNECTION ERROR] {error}'

    def sql_to_frame(self, filename):

        with open(filename, 'r') as file:
            query = file.read()

        dataframe = pd.read_sql(text(query), self.connection)

        return dataframe
    def frame_to_sql(self,dataframe:pd.DataFrame,tablename):
        try:
            dataframe.to_sql(tablename,self.connection)
        except ValueError as error:
            raise f'[UPDATE FAILED]{error}'

    def close(self):
        self.connection.close()

