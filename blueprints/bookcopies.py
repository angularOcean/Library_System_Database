from flask import Blueprint, Flask, render_template, request, redirect
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig
from forms import AddCopy

bookcopies_bp = Blueprint("bookcopies", __name__)

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

# -----------BOOKCOPIES-----------

# bookcopies.html
@bookcopies_bp.route("/bookcopies.html")
def bookcopies_page():
    query = """
    select BookCopies.copy_id, 
    Books.title,
        concat(Authors.author_first, ' ', Authors.author_last) as author_name,
        Locations.location_name
    from Locations
        right join BookCopies on Locations.location_id = BookCopies.location_id
        inner join Books on BookCopies.book_id = Books.book_id
        inner join Authors on Books.author_id = Authors.author_id
    order by Books.title asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    bookcopies_headings = ["Copy ID", "Title", "Author", "Location"]

    return render_template(
        "table_template.j2",
        title="Book Copies",
        description="This is a database of individual copies of books",
        headings=bookcopies_headings,
        data=results,
        routeURL="bookcopy",
    )


# To Bookcopies from Books
@bookcopies_bp.route("/bookcopies/<book_id>", methods=["POST", "GET"])
def go_to_bookcopies(book_id):
    # Initial Display
    query1 = """
    SELECT bookcopies.copy_id, bookcopies.book_id, locations.location_name
    FROM bookcopies
    INNER JOIN locations ON bookcopies.location_id = locations.location_id
    WHERE bookcopies.book_id = %s
    """
    curr = db.execute_query(
        db_connection=db_connection, query=query1, query_params=(book_id)
    )
    info = curr.fetchall()
    bookcopy_headings = ["Copy ID", "Book ID", "Location"]

    query2 = """
    SELECT
    Books.title, 
    concat(Authors.author_first, ' ', Authors.author_last) as author_name
    from Books
    left join Authors on Books.author_id = Authors.author_id
    WHERE books.book_id = %s
    """

    curr2 = db.execute_query(
        db_connection=db_connection, query=query2, query_params=(book_id)
    )
    titleinfo = curr2.fetchone()
    print(titleinfo)

    # Get Valid Locations Dropdown
    location_query = """SELECT location_id, location_name FROM Locations ORDER BY location_name ASC"""
    location_query = db.execute_query(db_connection=db_connection, query=location_query)
    location_results = list(location_query.fetchall())
    location_results.append((-1, "None"))

    # Intialize Add Book Copy Form
    add_copy_form = AddCopy()
    add_copy_form.location_dropdown.choices = location_results

    # Form submission
    if add_copy_form.validate_on_submit():
        input_location = add_copy_form.location_dropdown.data

        # Account for Null Location
        if input_location == "-1":
            add_copy_query = (
                """INSERT INTO BookCopies (book_id, location_id) VALUES (%s, NULL); """
            )
            add_copy_cursor = db.execute_query(
                db_connection=db_connection,
                query=add_copy_query,
                query_params=(book_id,),
            )
        else:
            # Insert Into Database
            add_copy_query = (
                """INSERT INTO BookCopies (book_id, location_id) VALUES (%s, %s); """
            )
            add_copy_cursor = db.execute_query(
                db_connection=db_connection,
                query=add_copy_query,
                query_params=(book_id, input_location),
            )

    return render_template(
        "table_bookcopies.j2",
        title=f"Book #{book_id}",
        headings=bookcopy_headings,
        data=info,
        description=f"For Book: '{titleinfo[0]}' by {titleinfo[1]}",
        routeURL="bookcopy",
        add_copy_form=add_copy_form,
    )


# @bookcopies_bp.route("/update_bookcopy/<int:id>", methods=["POST", "GET"])
# def bookcopy_edit(id):
#     pass


# bookcopies DELETE


@bookcopies_bp.route("/delete_bookcopy/<int:id>", methods=["POST", "GET"])
def bookcopy_delete(id):

    query1 = "select Books.book_id from BookCopies INNER JOIN Books ON BookCopies.book_id = Books.book_id WHERE BookCopies.copy_id  = %s;"
    cursor = db.execute_query(
        db_connection=db_connection,
        query=query1,
        query_params=(id,),
    )
    book_id = cursor.fetchone()

    query = "DELETE FROM BookCopies WHERE copy_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect(f"/bookcopies/{book_id[0]}")
