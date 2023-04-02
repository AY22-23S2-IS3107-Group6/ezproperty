from flask import Flask, jsonify
from flask_cors import CORS
from db import DataWarehouse

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
    return jsonify(warehouse.query("SELECT * FROM amn__SuperMarket"))

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
