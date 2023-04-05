import mysql.connector
from typing import List

from .mysql_connector import connect_to_mysql
from .schemas import create_queries, insert_queries


class DataWarehouse:
    def __init__(self, create_tables: bool = False, drop_tables: bool = False):
        self.db = connect_to_mysql()
        self.cursor = self.db.cursor(buffered=True)
        self.schemas = create_queries
        self.insert_queries = insert_queries
        self.start_db("is3107g6")
        if drop_tables: self.drop_schemas()
        if create_tables: self.load_schemas()

    def start_db(self, database: str):
        self.cursor.execute("SHOW DATABASES")
        databases = self.cursor.fetchall()

        if (database, ) not in databases:
            self.cursor.execute(f"CREATE DATABASE {database}")
            self.log(f"Database {database} created successfully.")

        self.cursor.execute(f"USE {database}")
        self.log(f"Using database {database}.")

    def load_schemas(self):
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        for schema_name in self.schemas:
            if (schema_name.lower(), ) not in tables:
                self.log(f"Table {schema_name} does not exist.")
                self.create_schema(schema_name)
            else:
                self.log(f"Table {schema_name} already exists.")

    def drop_schemas(self):
        for schema_name in self.schemas:
            self.drop_schema(schema_name)

    def create_schema(self, schema_name):
        try:
            self.cursor.execute(self.schemas[schema_name])
            self.db.commit()
            self.log(f"Table {schema_name} created successfully.")
        except mysql.connector.Error as err:
            self.log(f"Failed creating table: {err}")

    def drop_schema(self, schema_name):
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {schema_name}")
            self.db.commit()
            self.log(f"Table {schema_name} deleted successfully.")
        except mysql.connector.Error as err:
            self.log(f"Failed creating table: {err}")

    def insert_to_schema(self, schema_name, objects: List[tuple]):
        try:
            self.cursor.executemany(self.insert_queries[schema_name], objects)
            self.db.commit()
            self.log(
                f"{self.cursor.rowcount} values were inserted to {schema_name} successfully."
            )
        except mysql.connector.Error as err:
            self.log(f"Failed to insert: {err}")

    def query(self, query):
        try:
            self.cursor.execute(query)
            columns = self.cursor.description 
            self.log(f"Query executed successfully.")
            return [{columns[index][0]:column for index, column in enumerate(value)} for value in self.cursor.fetchall()]
        except mysql.connector.Error as err:
            self.log(f"Failed creating table: {err}")

    def update(self, update_query):
        try:
            self.cursor.execute(update_query)
            self.log(f"Update executed successfully.")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.log(f"Failed updating: {err}")

    def log(self, message: str):
        print(f"Database | {message}")
