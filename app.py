# ------- Citations ---------

# Citation for table_template:
# Date: 05/03/2022
# Based on:
# Source URL: https://www.youtube.com/watch?v=mCy52I4exTU

# Citation for app.py:
# Date: 05/03/2022
# Based on: OSU CS340 Flask Starter Guide
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, request, redirect
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig
import os

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
# AUTHORS
app.register_blueprint(authors_bp)

# BOOKS
app.register_blueprint(books_bp)

# BOOKCOPIES
app.register_blueprint(bookcopies_bp)

# PATRONS
app.register_blueprint(patrons_bp)

# CHECKOUTS
app.register_blueprint(checkouts_bp)

# CHECKEDBOOKS
app.register_blueprint(checkedbooks_bp)

# PUBLISHERS
app.register_blueprint(publishers_bp)

# LOCATIONS
app.register_blueprint(locations_bp)


# -----------HOME PAGE-----------
@app.route("/")
def index():
    return render_template("home_template.j2")


# Listener
# Port is 5000
if __name__ == "__main__":
    # #port = int(os.environ.get("PORT", 9112))
    # #                                ^^^^
    # #              You can replace this number with any valid port
    app.run()
