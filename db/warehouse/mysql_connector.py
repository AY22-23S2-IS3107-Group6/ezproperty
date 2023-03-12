import mysql.connector

def connect_to_mysql(database: str = None):
    host = "localhost"
    user = "root"
    print(f"Connecting to '{host}' with user '{user}'")
    if database is None:
        return mysql.connector.connect(
            host=host,
            user=user,
            password="password"
        )
    else:
        return mysql.connector.connect(
            host=host,
            user=user,
            password="password",
            database=database,
        )

