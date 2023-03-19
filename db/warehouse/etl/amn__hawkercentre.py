import pymongo
import pandas as pd
import mysql.connector
import requests
from sqlalchemy import create_engine
from warehouse.__init__ import DataWarehouse


def extract():

    # Fetch data sets
    respHawkerCentre = requests.get(
        'https://data.gov.sg/api/action/datastore_search?resource_id=8f6bba57-19fc-4f36-8dcf-c0bda382364d'
        .json())

    # Feed data into transformation
    transform(respHawkerCentre)


def transform(respPublic, respSeason):
    # merge
    # convert variables accordingly
    # remove grouped carparks
    # flatten coordinates
    table_name = "hawker centres"

    load(df, table_name)


def load(df, table_name):

    # load into mongodb

    data_warehouse = DataWarehouse()
    data_warehouse.insert_to_schema(self, INSERT_NAME, table_name)
