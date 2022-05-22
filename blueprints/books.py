#Books Page: Select, Insert, Update, Delete

from flask import Blueprint, Flask, render_template, request, redirect
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig

books_bp = Blueprint('books', __name__)

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

# -----------BOOKS-----------
# books.html
@books_bp .route("/books.html", methods=["POST", "GET"])
def books_page():
    # Initial Display
    query = """
    select Books.book_id,
    Books.isbn, 
        Books.title, 
        concat(Authors.author_first, ' ', Authors.author_last) as author_name,
        Publishers.publisher_name,
        Books.year
    from Books
        left join Authors on Books.author_id = Authors.author_id
        left join Publishers on Books.publisher_id = Publishers.publisher_id
    order by isbn asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    books_headings = ["ID", "ISBN", "Title", "Author", "Publisher", "Year"]

    # Get Valid Author Dropdown
    query2 = """SELECT author_id, concat(author_first, ' ', author_last) as author_name FROM Authors ORDER BY author_last ASC"""
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    results2 = cursor2.fetchall()

    # Get Valid Publisher Dropdown
    query3 = """SELECT publisher_id, publisher_name FROM Publishers ORDER BY publisher_name ASC"""
    cursor3 = db.execute_query(db_connection=db_connection, query=query3)
    results3 = cursor3.fetchall()

    # books INSERT
    if request.method == "POST":
        request.form.get("insert Books")
        input_isbn = request.form["ISBN"]
        input_title = request.form["Title"]
        input_author = request.form["Author"]
        input_publisher = request.form["Publisher"]
        input_year = request.form["Year"]
        query = """INSERT INTO Books (isbn, title, author_id, publisher_id, year) VALUES (%s, %s, %s, %s, %s); """
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(
                input_isbn,
                input_title,
                input_author,
                input_publisher,
                input_year,
            ),
        )
        return redirect("/books.html")

    return render_template(
        "table_template.j2",
        title="Books",
        description="This is a database of books.",
        headings=books_headings,
        data=results,
        author_dropdown=results2,
        publisher_dropdown=results3,
        routeURL="book",
    )


# books UPDATE
@books_bp .route("/update_book/<int:id>", methods=["GET", "POST"])
def books_edit(id):
    if request.method == "GET":
        query = """
        select Books.book_id,
        Books.isbn, 
        Books.title,
        Authors.author_id, 
        Publishers.publisher_id, 
        Books.year
        from Books
        left join Authors on Books.author_id = Authors.author_id
        left join Publishers on Books.publisher_id = Publishers.publisher_id
        where Books.book_id = %s;"""
        curr = db.execute_query(
            db_connection=db_connection, query=query, query_params=(id,)
        )
        info = curr.fetchone()

    books_edit_headings = [
        "ID",
        "ISBN",
        "Title",
        "Author ID",
        "Publisher ID",
        "Year",
    ]

    # Get Valid Author Dropdown
    query2 = """SELECT author_id, concat(author_first, ' ', author_last) as author_name FROM Authors ORDER BY author_last ASC"""
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    results2 = cursor2.fetchall()

    # Get Valid Publisher Dropdown
    query3 = """SELECT publisher_id, publisher_name FROM Publishers ORDER BY publisher_name ASC"""
    cursor3 = db.execute_query(db_connection=db_connection, query=query3)
    results3 = cursor3.fetchall()

    if request.method == "POST":
        request.form.get("Update Book")
        input_isbn = request.form["ISBN"]
        input_title = request.form["Title"]
        input_author = request.form["Author"]
        input_publisher = request.form["Publisher"]
        input_year = request.form["Year"]
        book_id = id
        query = "UPDATE Books SET isbn=%s, title=%s, author_id=%s, publisher_id=%s, year=%s WHERE book_id=%s;"
        curr = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(
                input_isbn,
                input_title,
                input_author,
                input_publisher,
                input_year,
                book_id,
            ),
        )
        return redirect("/books.html")

    return render_template(
        "update_book_template.j2",
        data=info,
        description="Editing Book: #",
        headings=books_edit_headings,
        title="Book",
        author_dropdown=results2,
        publisher_dropdown=results3,
        routeURL="books",
    )


# books DELETE
@books_bp .route("/delete_book/<int:id>", methods=["GET", "POST"])
def delete_book(id):
    query = "DELETE FROM Books WHERE book_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect("/books.html")