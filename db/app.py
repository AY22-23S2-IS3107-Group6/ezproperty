from flask import Flask, jsonify, request
from flask_cors import CORS
from db import DataWarehouse
from db.warehouse.schemas import create_queries

app = Flask(__name__)
CORS(app)

@app.route('/<category>/<schema>', methods=['GET'])
def getData(category: str, schema: str):
    if f"{category}__{schema}" not in [schema_name.lower() for schema_name in create_queries]:
        return "Bad request", 400
    warehouse = DataWarehouse()
    return jsonify(warehouse.query(f"SELECT * FROM {category}__{schema}"))


@app.route('/<category>/<schema>', methods=['POST'])
def createData(category: str, schema: str):
    if f"{category}__{schema}" not in [schema_name.lower() for schema_name in create_queries]:
        return "Content-Type not supported!", 400
    if request.headers.get('Content-Type') != 'application/json':
        return "Bad request", 400
    try:
        warehouse = DataWarehouse()
        warehouse.insert_to_schema(f"{category}__{schema}", request.json)
    except:
        return "Request failed", 500
    
