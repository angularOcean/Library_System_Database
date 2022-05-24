# Checkedbooks Page: Select
# https://stackoverflow.com/questions/61625290/flask-make-a-button-direct-to-another-page

from flask import Blueprint, Flask, render_template, request, redirect
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig

checkedbooks_bp = Blueprint("checkedbooks", __name__)


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

# -----------CHECKEDBOOKS-----------
# checkedbooks.html
@checkedbooks_bp.route("/checkedbooks.html")
def checkedbooks_page():
    query = """ 
    select 
    BookCopies.copy_id, 
    Books.title,
    concat(Patrons.patron_first, ' ', Patrons.patron_last) as patron_name,
    Checkouts.checkout_date,
    Checkouts.return_date,
    CheckedBooks.returned
    from Books
        inner join BookCopies on Books.book_id = BookCopies.book_id
        inner join CheckedBooks on BookCopies.copy_id = CheckedBooks.copy_id
        inner join Checkouts on Checkouts.checkout_id = CheckedBooks.checkout_id
        inner join Patrons on Patrons.patron_id = Checkouts.patron_id
    order by Checkouts.checkout_date desc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    checkedbooks_headings = [
        "Copy ID",
        "Book Title",
        "Patron Name",
        "Checkout Date",
        "Return Date",
        "Returned",
    ]

    return render_template(
        "table_template.j2",
        title="Checked Books",
        description="This is a read-only list of all checkout line items in the Penguin Library Database. Please edit any checkout information from the Checkouts page.",
        headings=checkedbooks_headings,
        data=results,
    )


# To CheckedBooks from Checkouts
@checkedbooks_bp.route("/checkedbooks/<checkout_id>", methods=["POST", "GET"])
def go_to_checkedbooks(checkout_id):
    # Initial Display:
    query = """
    SELECT Checkedbooks.checked_book_id, BookCopies.copy_id, Books.title, Locations.location_name, Checkouts.checkout_date, Checkouts.return_date, CheckedBooks.returned
    FROM Checkouts
    INNER JOIN CheckedBooks ON Checkouts.checkout_id = CheckedBooks.checkout_id
    INNER JOIN BookCopies ON CheckedBooks.copy_id = BookCopies.copy_id
    INNER JOIN Locations ON BookCopies.location_id = Locations.location_id
    INNER JOIN Books ON BookCopies.book_id = Books.book_id
    WHERE Checkouts.checkout_id = %s
    """
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(checkout_id)
    )
    info = curr.fetchall()
    checkedbooks_headings = [
        "ID",
        "Copy ID",
        "Book Title",
        "Copy Location",
        "Checkout Date",
        "Return Date",
        "Returned",
    ]

    checkoutid = checkout_id

    # Get Patron Name
    query2 = """
    SELECT concat(Patrons.patron_first, ' ', Patrons.patron_last) as patron_name
    FROM Patrons
    INNER JOIN Checkouts ON Patrons.patron_id = Checkouts.patron_id 
    WHERE Checkouts.checkout_id = %s
    """
    curr2 = db.execute_query(
        db_connection=db_connection, query=query2, query_params=(checkout_id)
    )
    info2 = curr2.fetchone()

    insert_headers = ["Copy ID", "Returned"]

    # checkedbook INSERT
    if request.method == "POST":
        request.form.get(f"insert Checkout #{checkout_id}")
        checkouts_id = checkout_id
        input_copyid = request.form["Copy ID"]
        input_returned = request.form["Returned"]
        query = f"""INSERT INTO Checkedbooks (checkout_id, copy_id, returned) VALUES (%s, %s, %s) ; """
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(checkouts_id, input_copyid, input_returned),
        )
        return redirect(request.url)

    return render_template(
        "table_checkedbooks.j2",
        title=f"Checkout #{checkout_id}",
        headings=checkedbooks_headings,
        data=info,
        description=f"For Patron: {info2[0]}",
        checkout_id=checkout_id,
        routeURL="checkedbook",
        form_headers=insert_headers,
    )


# checkedbooks UPDATE
@checkedbooks_bp.route("/update_checkedbook/<int:id>", methods=["POST", "GET"])
def checkedbooks_edit(id):
    query1 = "select checkout_id from checkedbooks where checked_book_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection,
        query=query1,
        query_params=(id,),
    )
    checkout_id = cursor.fetchall()

    if request.method == "GET":
        query2 = "SELECT returned from checkedbooks where checked_book_id = %s;"
        curr = db.execute_query(
            db_connection=db_connection, query=query2, query_params=(id,)
        )
        info = curr.fetchone()

    checkedbook_edit_headings = ["Returned"]

    if request.method == "POST":
        request.form.get("update Checked Book")
        checkedbook_returned = request.form["Returned"]
        checkedbook_id = id
        query = f"update Checkedbooks set returned = %s where checked_book_id = %s;"
        curr = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(checkedbook_returned, checkedbook_id),
        )
        return redirect(f"/checkedbooks/{checkout_id[0][0]}")

    return render_template(
        "update_checkedbook_template.j2",
        data=info,
        description=f"Editing Checked Book: # {id}",
        headings=checkedbook_edit_headings,
        title="Checked Book",
        routeURL="checkedbooks",
        checked_book_id=id,
    )


# checkedbook DELETE
@checkedbooks_bp.route("/delete_checkedbook/<int:id>", methods=["GET", "POST"])
def delete_checkedbook(id):
    query1 = "select checkout_id from checkedbooks where checked_book_id = %s;"
    cursor = db.execute_query(
        db_connection=db_connection,
        query=query1,
        query_params=(id,),
    )
    checkout_id = cursor.fetchall()

    query2 = "DELETE FROM checkedbooks WHERE checked_book_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query2, query_params=(id,)
    )
    return redirect(f"/checkedbooks/{checkout_id[0][0]}")
