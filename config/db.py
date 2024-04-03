import sqlalchemy

# Define the MariaDB engine using MariaDB Connector/Python
engine = sqlalchemy.create_engine(
    "mariadb+mariadbconnector://racuna:password@localhost:3306/storedb")

conn = engine.connect()
