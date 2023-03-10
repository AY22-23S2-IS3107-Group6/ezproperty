import mysql.connector

def connect_to_mysql():
    host = "localhost"
    user = "root"
    print(f"Connecting to '{host}' with user '{user}'")
    return mysql.connector.connect(
        host=host,
        user=user,
        password="password"
    )
