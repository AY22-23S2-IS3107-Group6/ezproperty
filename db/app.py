from flask import Flask, jsonify, request
from flask_cors import CORS
from db import DataWarehouse
import mysql.connector
from .utils import get_floor_range

app = Flask(__name__)
CORS(app)


@app.route('/propertytransaction')
def getPropertyTransactions():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM main__PropertyTransaction"))


@app.route('/rentaltransaction')
def getRentalTransactions():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM main__RentalTransaction"))


@app.route('/propertyinformation')
def getPropertyInformation():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM ref__PropertyInformation"))


@app.route('/district')
def getDistricts():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM ref__District"))


@app.route('/trainstation')
def getTrainStations():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM amn__TrainStation"))


@app.route('/primaryschool')
def getPrimarySchools():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM amn__PrimarySchool"))


@app.route('/supermarket')
def getSupermarkets():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM amn__Supermarket"))


@app.route('/hawkercentre')
def getHawkerCentres():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM amn__HawkerCentre"))


@app.route('/carparkpublic')
def getPublicCarparks():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM amn__CarparkPublic"))


@app.route('/carparkseasons')
def getSeasonCarparks():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM amn__CarparkSeason"))


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

        # prepare floor_start & floor_end to input into datawarehouse
        floor_range = get_floor_range(floor)
        floor_start = floor_range["floor_start"]
        floor_end = floor_range["floor_end"]

        # prepare resale boolean
        if (resale == "resale"):
            resale = True
        else:
            resale = False

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

        # warehouse = DataWarehouse()
        # warehouse.insert_to_schema("main__PropertyTransaction",
        #                            propertyTransaction)

        return futurePropertyTransaction
