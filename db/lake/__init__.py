from typing import List

from .mongodb_connector import connect_to_mongodb

class DataLake:
    def __init__(self, drop_tables: bool = False):
        self.db = connect_to_mongodb()
        if drop_tables: self.db.drop_database("is3107g6")
        self.start_db("is3107g6")

    def start_db(self, database: str):
        self.cursor = self.db[database]

    def insert_to_schema(self, schema_name, objects: List[dict]):
        try:
            self.cursor[schema_name].insert_many(objects)
        except:
            print(f"Failed inserting")

    def query(self, schema_name, query):
        try:
            return self.cursor[schema_name].aggregate(query)
        except:
            print(f"Failed querying")

    def query_find(self, schema_name, query):
        try:
            return self.cursor[schema_name].find(query)
        except:
            print(f"Failed querying")

    def delete_all_entries(self, schema_name):
        try:
            result = self.cursor[schema_name].delete_many({})
            print(f"Deleted {result.deleted_count} entries from {schema_name}")
        except:
            print(f"Failed deleting entries from {schema_name}")