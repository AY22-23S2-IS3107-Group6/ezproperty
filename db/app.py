from flask import Flask, jsonify, request
from flask_cors import CORS
from db import DataWarehouse
import mysql.connector

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

        # preparing data to be inserted into datawarehouse
        # prepare floor_start_range & floor_end_range
        def find_closest_floor_number(number, list_of_floor_numbers):
            closest_floor_number = None
            min_difference = float("inf")

            for num in list_of_floor_numbers:
                difference = abs(number - num)

                if difference < min_difference:
                    closest_floor_number = num
                    min_difference = difference

            return closest_floor_number

        def generate_incrementing_floor_numbers(start, end, increment):
            floor_numbers_list = []
            current_num = start

            while current_num <= end:
                floor_numbers_list.append(current_num)
                current_num += increment

            return floor_numbers_list

        floor_start_range = generate_incrementing_floor_numbers(1, 100, 5)
        floor_end_range = generate_incrementing_floor_numbers(5, 100, 5)

        if (floor == 0):
            floor_start = 0
            floor_end = 0
        else:
            floor_start = find_closest_floor_number(floor, floor_start_range)
            floor_end = find_closest_floor_number(floor, floor_end_range)


# check resale
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

        warehouse = DataWarehouse()
        warehouse.insert_to_schema("main__PropertyTransaction",
                                   propertyTransaction)

        # not sure what to return
        return "hi"