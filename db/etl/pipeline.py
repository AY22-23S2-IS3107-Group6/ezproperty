import pymongo
import mysql.connector
from ..lake import DataLake
from ..warehouse import DataWarehouse

class Pipeline:
    def __init__(self):
        self.dl = DataLake()
        self.dw = DataWarehouse()
        data = self.extract()
        transformed_data = self.transform(data)
        self.load(transformed_data)

    def extract(self) -> list:
        """ Extracts data from data source and ingest to data lake. """
        pass

    def transform(self, result: list) -> list:
        """ Transforms data extracted. """
        pass

    def load(self, result: list) -> None:
        """ Loads data into data warehouse. """
        self.dw_loader(result, self.schema_name)

    def dl_loader(self, result: list, schema_name: str) -> None:
        """ Loads data to data lake """
        try:
            self.log(schema_name, f"Loading {len(result)} documents to data lake.")
            self.dl.insert_to_schema(schema_name, result)
        except pymongo.errors.ConnectionFailure as err:
            self.log(schema_name, f"Connection to MongoDB failed: {err}.")
        except:
            self.log(schema_name, "Load process to data warehouse failed.")

    def dl_getter(self, schema_name: str) -> list:
        """ Gets data from data lake """
        try:
            self.log(schema_name, "Retreiving data from data lake with _id.")
            result = self.dl.query_find(schema_name, {})
            result = list(result)
            if (len(result) > 0):
                self.log(schema_name, f"Load success. Retrieved {len(result)} documents.")
            return result
        except pymongo.errors.ConnectionFailure as err:
            self.log(schema_name, f"Connection to MongoDB failed: {err}.")
        except:
            self.log(schema_name, "Load process from data lake failed.")

    def dw_loader(self, result: list, schema_name: str) -> None:
        """ Loads data to data warehouse """
        try:
            self.log(schema_name, f"Loading {len(result)} documents to data lake.")
            self.dw.insert_to_schema(schema_name, list(map(lambda x: tuple(x.values()), result)))

            self.log(schema_name, "Inserting to data warehouse.")
            output = self.dw.query(f"SELECT * FROM {schema_name}")
            if (len(output) > 0):
                self.log(schema_name, "Load process to data warehouse success. Printing first result.")
                print(output[0])
        except mysql.connector.Error as err:
            self.log(schema_name, f"Connection to data warehouse failed: {err}")
        except:
            self.log(schema_name, "Load process to data warehouse failed.")

    def log(self, schema_name: str, message: str):
        print(f"Pipeline | {schema_name.ljust(26)} | {message}")