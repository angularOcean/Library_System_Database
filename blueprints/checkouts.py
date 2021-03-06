# Checkouts Page: Select, Insert, Update, Delete and navigation to checkedbooks page
# CheckedBooks Insert, Update, and Delete from this page

from flask import Blueprint, Flask, render_template, request, redirect, g
import database.db_connector as db
import app

checkouts_bp = Blueprint("checkouts", __name__)

# -----------CHECKOUTS-----------

# checkouts.html
@checkouts_bp.route("/checkouts.html", methods=["POST", "GET"])
def checkouts_page():
    # Initial Display:
    query = """ 
    select
        Checkouts.checkout_id,
        concat(Patrons.patron_first, ' ', Patrons.patron_last) as patron_name,
        Checkouts.checkout_date,
        Checkouts.return_date
    from Patrons
        inner join Checkouts on Patrons.patron_id = Checkouts.patron_id
    order by Checkouts.checkout_id asc;
    """
    cursor = db.execute_query(db_connection=app.db_connection, query=query)
    results = cursor.fetchall()
    checkouts_headings = [
        "Checkout ID",
        "Patron Name",
        "Checkout Date",
        "Return Date",
    ]

    # Get Valid Patron Dropdown
    query2 = """SELECT patron_id, concat(patron_first, ' ', patron_last) as patron_name FROM Patrons ORDER BY patron_last ASC;"""
    cursor2 = db.execute_query(db_connection=app.db_connection, query=query2)
    results2 = cursor2.fetchall()

    # checkout INSERT
    if request.method == "POST":
        request.form.get("insert Checkouts")
        input_patron = request.form["patron_choice"]
        input_checkout_date = request.form["checkout_date_input"]
        input_return_date = request.form["return_date_input"]
        query = """INSERT INTO Checkouts (checkout_date, return_date, patron_id) VALUES (%s, %s, %s) ; """
        cursor = db.execute_query(
            db_connection=app.db_connection,
            query=query,
            query_params=(input_checkout_date, input_return_date, input_patron),
        )
        return redirect("/checkouts.html")

    return render_template(
        "table_template.j2",
        title="Checkouts",
        description="This is the checkout data for the Penguin Library System.",
        headings=checkouts_headings,
        data=results,
        name_dropdown=results2,
        routeURL="checkout",
    )


# checkouts UPDATE
@checkouts_bp.route("/update_checkout/<int:id>", methods=["GET", "POST"])
def checkouts_edit(id):
    if request.method == "GET":
        query = """
        SELECT Checkouts.checkout_id, Patrons.patron_id, Patrons.patron_first, Patrons.patron_last, Checkouts.checkout_date, Checkouts.return_date 
        FROM Patrons 
        INNER JOIN Checkouts ON Patrons.patron_id = Checkouts.patron_id 
        WHERE checkout_id = %s"""
        curr = db.execute_query(
            db_connection=app.db_connection, query=query, query_params=(id,)
        )
        info = curr.fetchone()
    checkouts_edit_headings = [
        "ID",
        "ID",
        "First Name",
        "Last Name",
        "Checkout Date",
        "Return Date",
    ]

    # Get Valid Patron Dropdown
    query2 = """SELECT patron_id, concat(patron_first, ' ', patron_last) as patron_name FROM Patrons ORDER BY patron_last ASC"""
    cursor2 = db.execute_query(db_connection=app.db_connection, query=query2)
    results2 = cursor2.fetchall()

    if request.method == "POST":
        request.form.get("Update Checkout")
        patron_choice = request.form["patron_choice"]
        checkout_date_input = request.form["checkout_date_input"]
        return_date_input = request.form["return_date_input"]
        checkout_id = id
        query = "UPDATE Checkouts SET patron_id = %s, checkout_date=%s, return_date=%s WHERE checkout_id=%s"
        curr = db.execute_query(
            db_connection=app.db_connection,
            query=query,
            query_params=(
                patron_choice,
                checkout_date_input,
                return_date_input,
                checkout_id,
            ),
        )
        return redirect("/checkouts.html")

    return render_template(
        "update_checkout_template.j2",
        data=info,
        description="Editing Checkout #",
        headings=checkouts_edit_headings,
        title="Checkout",
        name_dropdown=results2,
    )


# checkouts DELETE
@checkouts_bp.route("/delete_checkout/<int:id>", methods=["GET", "POST"])
def delete_checkout(id):
    query = "DELETE FROM Checkouts WHERE checkout_id = %s"
    curr = db.execute_query(
        db_connection=app.db_connection, query=query, query_params=(id,)
    )
    return redirect("/checkouts.html")
