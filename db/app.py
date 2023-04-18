from flask import Flask, json, jsonify, request
from flask_cors import CORS
from db import DataWarehouse
from .utils import get_floor_range
from db.warehouse.schemas import create_queries
import numpy as np
import pandas as pd

from db.ml import export_model 

app = Flask(__name__)
CORS(app)


@app.route('/<category>/<schema_name>', methods=['GET'])
def get_data(category: str, schema_name: str):
    schema = get_schema(category, schema_name)
    if not schema:
        return jsonify({"error": "Bad request"}), 400
    dw = DataWarehouse()
    return jsonify(dw.query(f"SELECT * FROM {schema}"))


@app.route('/<category>/<schema_name>', methods=['POST'])
def post_data(category: str, schema_name: str):
    schema = get_schema(category, schema_name)
    if not schema:
        return jsonify({"error": "Bad request"}), 400
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({"error": "Content-Type not supported!"}), 400
    try:
        dw = DataWarehouse()
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "JSON data must be a list"}), 400
        dw.insert_to_schema(f"{schema}", data)
        return "Successfully added"
    except:
        return "Request failed", 500


def get_schema(category: str, schema_name: str):
    for schema in create_queries:
        if f"{category}__{schema_name}" == schema.lower():
            return schema
    return None


@app.route('/addpropertytransaction', methods=['POST'])
def addPropertyTransaction():
    if request.method == "POST":
        # retrieve data from FE
        data = request.get_json()["values"]
        print(data)

        # separating data
        street = data["street"]
        floor = data["floor"]
        district = data["district"]
        propertyType = data["propertyType"]
        area = data["area"]
        price = data["price"]
        transactionDate = data["transactionDate"]
        tenure = data["tenure"]
        resale = data["resale"]

        # prepare floor_start & floor_end to input into datawarehouse
        # prepare floor_start & floor_end to input into datawarehouse
        floor_range = get_floor_range(floor)
        floor_start = floor_range["floor_start"]
        floor_end = floor_range["floor_end"]

        # prepare resale boolean
        if (resale == "resale"):
            resale = True
        else:
            resale = False

        propertyTransaction = [{
            "district": district,
            "street": street,
            "floorRangeStart": floor_start,
            "floorRangeEnd": floor_end,
            "propertyType": propertyType,
            "area": area,
            "price": price,
            "transactionDate": transactionDate,
            "tenure": tenure,
            "resale": resale
        }]
        propertyTransaction = list(
            map(lambda x: tuple(x.values()), propertyTransaction))
        print(propertyTransaction)

        warehouse = DataWarehouse()
        warehouse.insert_to_schema("main__PropertyTransaction",
                                   propertyTransaction)

        return propertyTransaction


@app.route('/predictpropertyprice', methods=['POST'])
def predictPropertyPrice():
    if request.method == "POST":
        # retrieve data from FE
        data = request.get_json()["values"]
        print(data)

        # separating data
        # street = data["street"]
        floor = data["floor"]
        district = data["district"]
        area = data["area"]
        transactionDate = data["transactionDate"]
        resale = data["resale"]

        # prepare floor_start & floor_end 
        floor_range = get_floor_range(floor)
        floor_start = floor_range["floor_start"]
        floor_end = floor_range["floor_end"]

        # prepare resale boolean
        if (resale == "resale"):
            resale = True
        else:
            resale = False

        # prepare date format
        df = pd.DataFrame(data, index=[0])
        for column in df.columns:
            if column == "transactionDate":
                df[column] = pd.to_datetime(df[column])
                df[column] = (df[column].max() - df[column]) / np.timedelta64(1,'Y')
                print(df[column][0])
                transactionDate = df[column][0]
        
        print(df)
        print(transactionDate)

        futurePropertyTransaction = [{
            "district": district,
            # "street": street,
            "floorRangeStart": floor_start,
            "floorRangeEnd": floor_end,
            "area": area,
            "transactionDate": transactionDate,
            "resale": resale
        }]
        futurePropertyTransaction = list(
            map(lambda x: tuple(x.values()), futurePropertyTransaction))
        print(futurePropertyTransaction)

        predicted_price = model.predict()
       
        return futurePropertyTransaction
