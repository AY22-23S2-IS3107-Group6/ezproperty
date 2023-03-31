from flask import Flask
from db import DataWarehouse

app = Flask(__name__)

@app.route('/propertyinfo')
def getPropertyRefs():
    warehouse = DataWarehouse()
    return warehouse.query("SELECT * FROM ref__PropertyInformation")