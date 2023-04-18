from flask import Flask, jsonify, request
from flask_cors import CORS
from db import DataWarehouse
from db.warehouse.schemas import create_queries

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

@app.route('/topfivedistrictsforapartment', methods=['GET'])
def get_top_five():
    dw = DataWarehouse()
    return jsonify(dw.query(f"SELECT propertyType, district, AVG(price) AS avg_price FROM main__propertyTransaction WHERE propertyType = 'Apartment' GROUP BY district ORDER BY avg_price DESC LIMIT 5"))

@app.route('/linechartdata', methods=['GET'])
def get_line_data():
    dw = DataWarehouse()
    return jsonify(dw.query(f"SELECT YEAR(transactionDate) AS year, AVG(price) AS avg_price FROM main__propertyTransaction WHERE propertyType = 'Apartment' GROUP BY year ORDER BY year"))

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

        # dummyInsert = [(14, 'WW', 46, 50, 'Apartment', 43, 900, '2023-04-10', 90, True)]

        warehouse = DataWarehouse()
        warehouse.insert_to_schema("main__PropertyTransaction",
                                   propertyTransaction)

        # not sure what to return
        return "hi"
