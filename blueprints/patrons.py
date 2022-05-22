#Patrons Page: Select, Insert, Update, Delete

from flask import Blueprint, Flask, render_template, request, redirect
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig

patrons_bp = Blueprint('patrons', __name__)

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

# -----------PATRONS-----------
# patrons.html 
@patrons_bp .route("/patrons.html", methods=["POST", "GET"])
def patrons_page():
    query = """ 
    select patron_id,
        patron_first,
        patron_last,
        email
    from Patrons
    order by patron_last asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    patrons_headings = ["ID", "First Name", "Last Name", "Email"]

    # patrons INSERT
    if request.method == "POST":
        request.form.get("insert Patrons")
        patron_first = request.form["First Name"]
        patron_last = request.form["Last Name"]
        patron_email = request.form["Email"]
        query = f"INSERT INTO Patrons(patron_first, patron_last, email) VALUES (%s, %s, %s);"
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(patron_first, patron_last, patron_email),
        )
        return redirect("/patrons.html")

    return render_template(
        "table_template.j2",
        title="Patrons",
        description="This is a database of patrons.",
        headings=patrons_headings,
        data=results,
        routeURL="patron",
    )


# patrons UPDATE
@patrons_bp .route("/update_patron/<int:id>", methods=["POST", "GET"])
def patrons_edit(id):
    if request.method == "GET":
        query = "SELECT patron_id, patron_first, patron_last, email FROM Patrons WHERE patron_id = %s"
        curr = db.execute_query(
            db_connection=db_connection, query=query, query_params=(id,)
        )
        info = curr.fetchall()
        print(info)

    patrons_edit_headings = ["ID", "First Name", "Last Name", "Email"]

    if request.method == "POST":
        request.form.get("Update Patron")
        patron_first = request.form["First Name"]
        patron_last = request.form["Last Name"]
        patron_email = request.form["Email"]
        patron_id = id
        query = "update Patrons set patron_first = %s, patron_last = %s, email = %s where patron_id = %s;"
        curr = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(patron_first, patron_last, patron_email, patron_id),
        )
        return redirect("/patrons.html")

    return render_template(
        "update_template.j2",
        data=info,
        description="Editing Patron: #",
        headings=patrons_edit_headings,
        title="Patrons",
        routeURL="patrons",
    )


# patrons DELETE
@patrons_bp .route("/delete_patron/<int:id>", methods=["GET", "POST"])
def delete_patron(id):
    query = "DELETE FROM Patrons WHERE patron_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect("/patrons.html")