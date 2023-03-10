from .mysql_connector import connect_to_mysql

class DataWarehouse:
    def __init__(self):
        self.db = connect_to_mysql()