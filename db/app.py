from flask import Flask, jsonify
from flask_cors import CORS
from db import DataWarehouse

def createApp():
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/propertyinfo')
    def getPropertyRefs():
        warehouse = DataWarehouse()
        return jsonify(warehouse.query("SELECT * FROM ref__PropertyInformation"))

    @app.route('/trainstation')
    def getTrainStations():
        warehouse = DataWarehouse()
        return jsonify(warehouse.query("SELECT * FROM amn__TrainStation"))
    
    return app

if __name__ == '__main__':
    app = createApp()
    app.run()