# ------- Citations ---------

# Citation for table_template:
# Date: 05/03/2022
# Based on:
# Source URL: https://www.youtube.com/watch?v=mCy52I4exTU

# Citation for app.py:
# Date: 05/03/2022
# Based on: OSU CS340 Flask Starter Guide
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

# Citation for database initialization code:
# Date: 05/09/2022
# Based on: CS340 Flask-starter-app guide on Github
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/database/db_connector.py

# Citation for database connection teardown
# Date: 06/03/2022
# Based on: Flaskr Tutorial about App Context
# Source URL: https://flask.palletsprojects.com/en/2.1.x/appcontext/

from flask import Flask, render_template, request, redirect, g
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig
import os
import pymysql

# -----------IMPORT BLUEPRINTS FOR ENTITIES-----------
from blueprints.authors import authors_bp
from blueprints.patrons import patrons_bp
from blueprints.locations import locations_bp
from blueprints.publishers import publishers_bp
from blueprints.books import books_bp
from blueprints.checkouts import checkouts_bp
from blueprints.bookcopies import bookcopies_bp
from blueprints.checkedbooks import checkedbooks_bp

# Configuration
app = Flask(__name__)
with app.app_context():
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
        db_connection = db.connect_to_database(
            ProductionConfig.DB_HOST,
            ProductionConfig.DB_USER,
            ProductionConfig.DB_PASSWORD,
            ProductionConfig.DB_NAME,
        )
    else:
        app.config.from_object("config.DevelopmentConfig")
        db_connection = db.connect_to_database(
            DevelopmentConfig.DB_HOST,
            DevelopmentConfig.DB_USER,
            DevelopmentConfig.DB_PASSWORD,
            DevelopmentConfig.DB_NAME,
        )

    # -----------REGISTOR BLUEPRINTS-----------
    app.register_blueprint(authors_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(bookcopies_bp)
    app.register_blueprint(patrons_bp)
    app.register_blueprint(checkouts_bp)
    app.register_blueprint(checkedbooks_bp)
    app.register_blueprint(publishers_bp)
    app.register_blueprint(locations_bp)

# -----------HOME PAGE-----------
@app.route("/")
def index():
    return render_template("home_template.j2")


# ------ CONNECTION TEARDOWN -----------
@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db_connection', None)

    if db is not None:
        db.close()

# Listener
# Port is 5000
if __name__ == "__main__":
    # #port = int(os.environ.get("PORT", 9112))
    # #                                ^^^^
    # #              You can replace this number with any valid port
    app.run()

