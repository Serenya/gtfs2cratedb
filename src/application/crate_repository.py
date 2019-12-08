import os
from crate import client
from crate.client.exceptions import ProgrammingError

CRATE_DB_HOST = os.environ.get('CRATE_DB_HOST', default='localhost:4200')


# Persistance layer that abstracts CrateDB
class CrateRepository:

    def __init__(self):
        connection = client.connect(CRATE_DB_HOST, error_trace=True)
        self.__cursor__ = connection.cursor()

    def create_table(self, table_name, columns):
        try:
            create_query = """CREATE TABLE {} ({})""".format(
                table_name,
                ', '.join([c + ' STRING' for c in columns])
            )
            self.__cursor__.execute(create_query)
        except ProgrammingError as e:
            if "RelationAlreadyExists" not in e.message:
                raise

    def insert_values(self, table_name, columns, values):
        insert_query = """INSERT INTO {} ({}) VALUES ({})""".format(
            table_name,
            ', '.join(columns),
            ', '.join('?' * len(columns)))
        self.__cursor__.executemany(insert_query, values)