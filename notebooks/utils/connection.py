import os

import sqlalchemy
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


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
    
    def frame_to_sql(self, dataframe, table_name):
        
        dataframe.to_sql(table_name, self.connection, if_exists='replace', index=True)
        
        return True

    def close(self):
        self.connection.close()
