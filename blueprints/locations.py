#Locations Page: Select, Insert, Update, Delete

from flask import Blueprint, Flask, render_template, request, redirect
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig

locations_bp = Blueprint('locations', __name__)

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

# -----------LOCATIONS-----------
# locations.html
@locations_bp.route("/locations.html", methods=["POST", "GET"])
def locations_page():
    query = """ 
    select location_id,
    location_name,
    location_address
    from Locations
    order by location_id asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    locations_headings = ["ID", "Name", "Address"]

    # locations INSERT
    if request.method == "POST":
        request.form.get("insert Library Locations")
        loc_name = request.form["Name"]
        loc_address = request.form["Address"]
        query = (
            f"INSERT INTO Locations(location_name, location_address) VALUES (%s,%s); "
        )
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(loc_name, loc_address),
        )
        return redirect("/locations.html")

    # render template
    return render_template(
        "table_template.j2",
        title="Library Locations",
        description="This is the location data for the Penguin Library System.",
        headings=locations_headings,
        data=results,
        routeURL="location",
    )


# locations UPDATE
@locations_bp.route("/update_location/<int:id>", methods=["POST", "GET"])
def locations_edit(id):
    if request.method == "GET":
        query = "SELECT location_name, location_address FROM Locations WHERE location_id = %s"
        curr = db.execute_query(
            db_connection=db_connection, query=query, query_params=(id,)
        )
        info = curr.fetchall()
        print(info)

    locations_edit_headings = ["Name", "Address"]

    if request.method == "POST":
        request.form.get("Update Location")
        loc_name = request.form["Name"]
        loc_address = request.form["Address"]
        loc_id = id
        query = f"update Locations set location_name = %s, location_address = %s where location_id = %s;"
        curr = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(loc_name, loc_address, loc_id),
        )
        return redirect("/locations.html")

    return render_template(
        "update_template.j2",
        data=info,
        description="Editing library location: ",
        headings=locations_edit_headings,
        title="Location",
        routeURL="locations",
    )


# locations DELETE
@locations_bp.route("/delete_location/<int:id>", methods=["GET", "POST"])
def delete_location(id):
    query = "DELETE FROM Locations WHERE location_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect("/locations.html")