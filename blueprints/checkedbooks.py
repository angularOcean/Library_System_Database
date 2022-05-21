from flask import Blueprint, Flask, render_template, request, redirect
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig

checkedbooks_bp = Blueprint('checkedbooks', __name__)

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


# checkedbooks INSERT


# checkedbooks UPDATE


# checkedbooks DELETE
