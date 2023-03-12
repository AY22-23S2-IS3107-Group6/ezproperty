import mysql.connector

from .mysql_connector import connect_to_mysql
from .schemas import schemas

class DataWarehouse:
    def __init__(self):
        self.db = connect_to_mysql()
        self.cursor = self.db.cursor(buffered=True)
        self.schemas = schemas
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
                self.create_table(schema_name)
            else:
                print(f"Table {schema_name} already exists.")

    def create_table(self, schema_name):
        try:
            self.cursor.execute(self.schemas[schema_name])
            print(f"Table {schema_name} created successfully.")
        except mysql.connector.Error as err:
            print(f"Failed creating table: {err}")
