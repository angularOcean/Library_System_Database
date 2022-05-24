# Books Page: Select, Insert, Update, Delete

from flask import Blueprint, Flask, render_template, request, redirect
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig
from forms import AuthorsFilter, AddBook

books_bp = Blueprint("books", __name__)

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
@books_bp.route("/books.html", methods=["POST", "GET"])
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

    # Set up Dropdowns for Filter and Add Book Forms
    author_query = """SELECT author_id, concat(author_first, ' ', author_last) as author_name FROM Authors ORDER BY author_last ASC"""
    author_cursor = db.execute_query(db_connection=db_connection, query=author_query)
    author_results = list(author_cursor.fetchall())
    author_form = AuthorsFilter()
    author_form.author_dropdown.choices = author_results
    selected_author = None

    add_book_form = AddBook()
    add_book_form.author_dropdown.choices = author_results

    publisher_query = """SELECT publisher_id, publisher_name FROM Publishers ORDER BY publisher_name ASC"""
    publisher_cursor = db.execute_query(
        db_connection=db_connection, query=publisher_query
    )
    publisher_results = publisher_cursor.fetchall()
    add_book_form.publisher_dropdown.choices = publisher_results

    # Intialize form results to None
    selected_author = None

    return render_template(
        "table_books.j2",
        title="Books",
        description="This is a database of books.",
        headings=books_headings,
        data=results,
        routeURL="book",
        author_form=author_form,
        add_book_form=add_book_form,
        selected_author=selected_author,
    )


# Books -- Filter By Author
@books_bp.route("/books/author", methods=["POST", "GET"])
def books_by_author():
    # Initialize Author Filter Form
    selected_author = None
    author_query = """SELECT author_id, concat(author_first, ' ', author_last) as author_name FROM Authors ORDER BY author_last ASC"""
    author_cursor = db.execute_query(db_connection=db_connection, query=author_query)
    author_results = author_cursor.fetchall()
    author_form = AuthorsFilter()
    author_form.author_dropdown.choices = author_results

    # If Someone Submits the Author Filter Form
    if author_form.validate_on_submit():
        selected_author = author_form.author_dropdown.data

    # Intialize Book Table
    filter_query = """
    select Books.book_id,
    Books.isbn, 
        Books.title,
        Publishers.publisher_name,
        Books.year
    from Books
        left join Authors on Books.author_id = Authors.author_id
        left join Publishers on Books.publisher_id = Publishers.publisher_id
    where Authors.author_id = %s
    order by isbn asc;
    """
    filter_cursor = db.execute_query(
        db_connection=db_connection, query=filter_query, query_params=(selected_author,)
    )
    filter_results = filter_cursor.fetchall()

    books_headings = ["ID", "ISBN", "Title", "Publisher", "Year"]

    # Grab Author's Name for Page Information
    selected_query = "select concat(Authors.author_first, ' ', Authors.author_last) as author_name from Authors where Authors.author_id = %s"
    selected_cursor = db.execute_query(
        db_connection=db_connection,
        query=selected_query,
        query_params=(int(selected_author),),
    )
    selected_results = selected_cursor.fetchone()

    # Initialize Add Book Form
    add_book_form = AddBook()

    return render_template(
        "table_books.j2",
        title=f"Books by {selected_results[0]}",
        author_form=author_form,
        add_book_form=add_book_form,
        selected_author=selected_author,
        headings=books_headings,
        data=filter_results,
        routeURL="book",
    )


# books INSERT/ADD
@books_bp.route("/add_book", methods=["POST", "GET"])
def books_add():
    input_isbn = None
    input_title = None
    input_author = None
    input_publisher = None
    input_year = None

    selected_author = None
    author_form = AuthorsFilter()
    add_book_form = AddBook()

    # Get Valid Author Dropdown
    author_query = """SELECT author_id, concat(author_first, ' ', author_last) as author_name FROM Authors ORDER BY author_last ASC"""
    author_query = db.execute_query(db_connection=db_connection, query=author_query)
    author_results = author_query.fetchall()
    add_book_form.author_dropdown.choices = author_results
    author_form.author_dropdown.choices = author_results

    # Get Valid Publisher Dropdown
    publisher_query = """SELECT publisher_id, publisher_name FROM Publishers ORDER BY publisher_name ASC"""
    publisher_cursor = db.execute_query(
        db_connection=db_connection, query=publisher_query
    )
    publisher_results = publisher_cursor.fetchall()
    add_book_form.publisher_dropdown.choices = publisher_results

    # Form submission
    if add_book_form.validate_on_submit():
        input_isbn = add_book_form.isbn.data
        input_title = add_book_form.title.data
        input_author = add_book_form.author_dropdown.data
        input_publisher = add_book_form.publisher_dropdown.data
        input_year = add_book_form.year.data

        # Insert Into Database
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


# books UPDATE
@books_bp.route("/update_book/<int:id>", methods=["GET", "POST"])
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
@books_bp.route("/delete_book/<int:id>", methods=["GET", "POST"])
def delete_book(id):
    query = "DELETE FROM Books WHERE book_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect("/books.html")
