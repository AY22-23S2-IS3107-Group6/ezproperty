from flask import Flask, json, jsonify, request
from flask_cors import CORS
from db import DataWarehouse
from .utils import get_floor_range
from db.warehouse.schemas import create_queries
import numpy as np
import pandas as pd
from datetime import date
from .ml.predictPrice import update_model, load_from_db_and_predict

app = Flask(__name__)
CORS(app)

@app.route('/<category>/<schema_name>', methods=['GET'])
def get_data(category: str, schema_name: str):
    schema = get_schema(category, schema_name)
    if not schema:
        return jsonify({"error": "Bad request"}), 400
    dw = DataWarehouse()
    return jsonify(dw.query(f"SELECT * FROM {schema} LIMIT 100"))


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

@app.route('/topfivedistrictsfor/<property_type>', methods=['GET'])
def get_top_five(property_type: str):
    dw = DataWarehouse()
    return jsonify(dw.query(f"SELECT propertyType, district, AVG(price) AS avg_price FROM main__propertyTransaction WHERE propertyType = '{property_type}' GROUP BY district ORDER BY avg_price DESC LIMIT 5"))

@app.route('/linechartdatafor/<property_type>', methods=['GET'])
def get_line_data(property_type: str):
    dw = DataWarehouse()
    return jsonify(dw.query(f"SELECT YEAR(transactionDate) AS year, AVG(price) AS avg_price FROM main__propertyTransaction WHERE propertyType = '{property_type}' GROUP BY year ORDER BY year"))

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

        # insert new property transaction
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
        
        # update price prediction model
        update_model()

        return jsonify(propertyTransaction)


@app.route('/predictpropertyprice', methods=['GET'])
def predictPropertyPrice():
    if request.method == "GET":
        # retrieve data from FE
        floor = int(request.args.get("floor"))
        district = int(request.args.get("district"))
        area = int(request.args.get("area"))
        transactionDate = request.args.get("transactionDate")
        resale = request.args.get("resale")

        # # prepare floor_start & floor_end 
        floor_range = get_floor_range(floor)
        floor_start = floor_range["floor_start"]
        floor_end = floor_range["floor_end"]

        # # prepare resale boolean
        if (resale == "resale"):
            resale = True
        else:
            resale = False

        # # prepare date format
        data = [{
            "floor": floor,
            "district": district,
            "area": area,
            "transactionDate": transactionDate,
            "resale": resale
        }]
        df = pd.DataFrame(data, index=[0])
        for column in df.columns:
            if column == "transactionDate":
                df[column] = pd.to_datetime(df[column])
                df[column] = (df[column] - pd.to_datetime(date.today())) / np.timedelta64(1,'Y')
                print(df[column][0])
                transactionDate = df[column][0]

        print(transactionDate)

        # get predict price from ML
        predicted_price = load_from_db_and_predict(district, floor_start, floor_end, area/100, transactionDate, resale)
        predicted_price = round(predicted_price[0][0], 2)
        print(type(predicted_price))
       
        return jsonify(str(predicted_price))
