from flask import Flask, jsonify
from flask_cors import CORS
from db import DataWarehouse

app = Flask(__name__)
CORS(app)

@app.route('/propertyinfo')
def getPropertyRefs():
    warehouse = DataWarehouse()
    return jsonify(warehouse.query("SELECT * FROM ref__PropertyInformation"))