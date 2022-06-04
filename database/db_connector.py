import pymysql
from flask import g

# -------- DATABASE -------------
def connect_to_database(host, user, passwd, db):
    """
    connects to a database and returns a database objects
    """
    if "db_connection" not in g:
        g.db_connection = pymysql.connect(host=host, user=user, password=passwd, database=db)
    return g.db_connection

def execute_query(db_connection=None, query=None, query_params=()):
    """
    executes a given SQL query on the given db connection and returns a Cursor object
    """
    if db_connection is None:
        print(
            "No connection to the database found! Have you called connect_to_database() first?"
        )
        return None

    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None

    print("Executing %s with %s" % (query, query_params))

    cursor = db_connection.cursor()
    cursor.execute(query, query_params)
    db_connection.commit()
    return cursor

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db_connection", None)

    if db is not None:
        db.close()
