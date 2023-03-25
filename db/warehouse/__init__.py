import mysql.connector
from typing import List

from .mysql_connector import connect_to_mysql
from .schemas import create_queries, insert_queries

class DataWarehouse:
    def __init__(self):
        self.db = connect_to_mysql()
        self.cursor = self.db.cursor(buffered=True)
        self.schemas = create_queries
        self.insert_queries = insert_queries
        self.start_db("is3107g6")
        self.load_schemas()

    def start_db(self, database: str):
        self.cursor.execute("SHOW DATABASES")
        databases = self.cursor.fetchall()
        
        if (database,) not in databases:
            self.cursor.execute(f"CREATE DATABASE {database}") 
            print(f"Database {database} created successfully.")
        
        self.cursor.execute(f"USE {database}")
        print(f"Using database {database}.")

    def load_schemas(self):
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        for schema_name in self.schemas:
            if (schema_name.lower(),) not in tables:
                print(f"Table {schema_name} does not exist.")
                self.create_schema(schema_name)
            else:
                print(f"Table {schema_name} already exists.")

    def create_schema(self, schema_name):
        try:
            self.cursor.execute(self.schemas[schema_name])
            self.db.commit()
            print(f"Table {schema_name} created successfully.")
        except mysql.connector.Error as err:
            print(f"Failed creating table: {err}")

    def insert_to_schema(self, schema_name, objects: List[tuple]):
        try:
            self.cursor.executemany(self.insert_queries[schema_name], objects)
            self.db.commit()
            print(f"{self.cursor.rowcount} values were inserted to {schema_name} successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to insert: {err}")

    def query(self, query):
        try:
            self.cursor.execute(query)
            print(f"Query executed successfully.")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Failed creating table: {err}")