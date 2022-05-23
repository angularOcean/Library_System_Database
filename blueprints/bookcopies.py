from flask import Blueprint, Flask, render_template, request, redirect
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig

bookcopies_bp = Blueprint('bookcopies', __name__)

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
    bookcopies_headings = ["ID", "Title", "Author", "Location"]

    # Get Valid Locations Dropdown
    query2 = """SELECT location_id, location_name FROM Locations ORDER BY location_name ASC"""
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    results2 = cursor2.fetchall()

    return render_template(
        "table_template.j2",
        title="Book Copies",
        description="This is a database of individual copies of books",
        headings=bookcopies_headings,
        data=results,
        locations_dropdown=results2,
        routeURL="bookcopy",
    )


# Dynamically Display Checked Out Books
@bookcopies_bp.route("/bookcopies/checked-out")
def show_checked_out():
    query = """
    select 
    BookCopies.copy_id,
    Books.title,
    concat(Authors.author_first, ' ', Authors.author_last) as author_name,
    Locations.location_name,
    Checkouts.checkout_date,
    Checkouts.return_date
    from Locations
    right join BookCopies on Locations.location_id = BookCopies.location_id
    inner join Books on BookCopies.book_id = Books.book_id
    inner join Authors on Books.author_id = Authors.author_id
    inner join CheckedBooks on BookCopies.copy_id = CheckedBooks.copy_id
    inner join Checkouts on CheckedBooks.checkout_id = Checkouts.checkout_id
    where CheckedBooks.returned = 0
    order by Books.title asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    checked_out_headings = [
        "ID",
        "Title",
        "Author",
        "Location",
        "Checkout Date",
        "Return Date",
    ]

    # Get Valid Locations Dropdown
    query2 = """SELECT location_id, location_name FROM Locations ORDER BY location_name ASC"""
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    results2 = cursor2.fetchall()

    return render_template(
        "table_template.j2",
        title="Checked Out Books",
        description="This is a list of all book copies currently checked out.",
        headings=checked_out_headings,
        data=results,
        locations_dropdown=results2,
        routeURL="bookcopy",
    )


# Dynamically Display Returned Books (On Shelf)
@bookcopies_bp.route("/bookcopies/on-shelf")
def show_on_shelf():
    query = """
    select BookCopies.copy_id,
    Books.title,
    concat(Authors.author_first, ' ', Authors.author_last) as author_name,
    Locations.location_name
    from BookCopies
    left join Locations on BookCopies.location_id = Locations.location_id
    left join CheckedBooks on BookCopies.copy_id = CheckedBooks.copy_id
    inner join Books on BookCopies.book_id = Books.book_id
    inner join Authors on Books.author_id = Authors.author_id
    where (CheckedBooks.returned is null
    or CheckedBooks.returned = 1)
    group by BookCopies.copy_id
    order by Books.title asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    on_shelf_headings = ["ID", "Title", "Author", "Location"]

    # Get Valid Locations Dropdown
    query2 = """SELECT location_id, location_name FROM Locations ORDER BY location_name ASC"""
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    results2 = cursor2.fetchall()

    return render_template(
        "table_template.j2",
        title="Books on the Shelf",
        description="This is a list of all book copies currently on the shelf.",
        headings=on_shelf_headings,
        data=results,
        locations_dropdown=results2,
        routeURL="bookcopy",
    )


# To Bookcopies from Books
@bookcopies_bp.route("/bookcopies/<book_id>", methods = ["POST", "GET"] )
def go_to_bookcopies(book_id):
    #Initial Display 
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
    bookcopy_headings = [
        "ID",
        "Book ID",
        "Location"
    ]

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
    titleinfo = curr2.fetchall()

    return render_template(
        "table_bookcopies.j2",
        title=f"Book #{book_id}",
        headings= bookcopy_headings,
        data=info,
        description=f"For Book: '{titleinfo[0][0]}' by {titleinfo[0][1]}",
        routeURL="bookcopy"
    )

# bookcopies DELETE