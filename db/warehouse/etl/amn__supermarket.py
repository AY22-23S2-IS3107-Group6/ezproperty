import pymongo
import pandas as pd
import mysql.connector
import requests
from sqlalchemy import create_engine
from warehouse.__init__ import DataWarehouse


def extract():

    # Fetch data sets
    respSupermarket = requests.get(
        'https://data.gov.sg/api/action/datastore_search?resource_id=3561a136-4ee4-4029-a5cd-ddf591cce643'
        .json())

    # Feed data into transformation
    transform(respSupermarket)


def transform(respPublic, respSeason):
    # merge
    # convert variables accordingly
    # remove grouped carparks
    # flatten coordinates
    table_name = ""

    load(df, table_name)


def load(df, table_name):
    # load into mongodb

    data_warehouse = DataWarehouse()
    data_warehouse.insert_to_schema(self, INSERT_NAME, table_name)
