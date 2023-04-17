from flask import Flask, json, jsonify, request
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
