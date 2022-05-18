# ------- Citations ---------

# Citation for table_template:
# Date: 05/03/2022
# Based on:
# Source URL: https://www.youtube.com/watch?v=mCy52I4exTU

# Citation for app.py:
# Date: 05/03/2022
# Based on: OSU CS340 Flask Starter Guide
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, json, request, redirect
import os
import pymysql
from flask import request
import database.db_connector as db
from config import DevelopmentConfig, ProductionConfig

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


# Routes
@app.route("/")
def index():
    return render_template("main.j2")


# 1. index.html
# render a navigation bar
@app.route("/index.html")
def root():
    return render_template("main.j2")


# -----------AUTHORS-----------
# 2. authors.html
@app.route("/authors.html", methods=["POST", "GET"])
def authors_page():
    # Initial Display:
    query = "select author_id, author_first, author_last from Authors order by author_last asc;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    authors_headings = ["ID", "First Name", "Last Name"]

    # author INSERT
    if request.method == "POST":
        request.form.get("insert Authors")
        author_fname = request.form["First Name"]
        author_lname = request.form["Last Name"]
        query = f"INSERT INTO Authors(author_first, author_last) VALUES (%s,%s); "
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(author_fname, author_lname),
        )
        return redirect("/authors.html")

    return render_template(
        "table_template.j2",
        title="Authors",
        description="This is a list of authors.",
        headings=authors_headings,
        routeURL="author",
        data=results,
    )


# author UPDATE
@app.route("/update_author/<int:id>", methods=["POST", "GET"])
def authors_edit(id):
    if request.method == "GET":
        query = "SELECT author_id, author_first, author_last FROM Authors WHERE author_id = %s"
        curr = db.execute_query(
            db_connection=db_connection, query=query, query_params=(id,)
        )
        info = curr.fetchall()

    authors_edit_headings = ["ID", "First Name", "Last Name"]

    if request.method == "POST":
        request.form.get("Update Author")
        author_fname = request.form["First Name"]
        author_lname = request.form["Last Name"]
        auth_id = id
        query = f"update Authors set author_first = %s, author_last = %s where author_id = %s;"
        curr = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(author_fname, author_lname, auth_id),
        )
        return redirect("/authors.html")

    return render_template(
        "update_template.j2",
        data=info,
        description="Editing Author: ",
        headings=authors_edit_headings,
        title="Author",
    )


# authors DELETE
@app.route("/delete_author/<int:id>", methods=["GET", "POST"])
def delete_author(id):
    query = "DELETE FROM Authors WHERE author_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect("/authors.html")


# -----------BOOKS-----------
# 3. books.html
@app.route("/books.html")
def books_page():
    query = """
    select Books.isbn, 
        Books.title, 
        Books.year,
        Authors.author_first,
        Authors.author_last,
        Publishers.publisher_name
    from Books
        inner join Authors on Books.author_id = Authors.author_id
        inner join Publishers on Books.publisher_id = Publishers.publisher_id
    order by isbn asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    books_headings = [
        "ISBN",
        "Title",
        "Year",
        "Author First",
        "Author Last",
        "Publisher",
    ]
    return render_template(
        "table_template.j2",
        title="Books",
        description="This is a database of books.",
        headings=books_headings,
        data=results,
    )


# books INSERT


# books DELETE


# -----------BOOKCOPIES-----------

# 4. bookcopies.html
@app.route("/bookcopies.html")
def bookcopies_page():
    query = """
    select Books.title,
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
    bookcopies_headings = ["Title", "Author", "Location"]
    return render_template(
        "table_template.j2",
        title="Book Copies",
        description="This is a database of individual copies of books",
        headings=bookcopies_headings,
        data=results,
    )


# 4.1 Dynamically Display Checked Out Books
@app.route("/bookcopies/checked-out")
def show_checked_out():
    query = """
    select Books.title,
    concat(Authors.author_first, ' ', Authors.author_last) as author_name,
    Locations.location_name,
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
    checked_out_headings = ["Title", "Author" "Location"]
    return render_template(
        "table_template.j2",
        title="Checked Out Books",
        description="This is a list of all book copies currently checked out.",
        headings=checked_out_headings,
        data=results,
    )


# 4.2 Dynamically Display Returned Books (On Shelf)
@app.route("/bookcopies/on-shelf")
def show_on_shelf():
    query = """
    select Books.title,
    concat(Authors.author_first, ' ', Authors.author_last) as author_name,
    Locations.location_name
    from Locations
    right join BookCopies on Locations.location_id = BookCopies.location_id
    inner join CheckedBooks on BookCopies.copy_id = CheckedBooks.copy_id
    inner join Books on BookCopies.book_id = Books.book_id
    inner join Authors on Books.author_id = Authors.author_id
    where CheckedBooks.returned is null
    or CheckedBooks.returned = 1
    order by Books.title asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    on_shelf_headings = ["Title", "Author", "Location"]
    return render_template(
        "table_template.j2",
        title="Books on the Shelf",
        description="This is a list of all book copies currently on the shelf.",
        headings=on_shelf_headings,
        data=results,
    )


# bookcopies DELETE


# -----------PATRONS-----------
# 5. patrons.html - Herakles
@app.route("/patrons.html")
def patrons_page():
    query = """ 
    select patron_first,
        patron_last,
        email
    from Patrons
    order by patron_last asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    patrons_headings = ["First Name", "Last Name", "Email"]
    return render_template(
        "table_template.j2",
        title="Patrons",
        description="This is a database of patrons.",
        headings=patrons_headings,
        data=results,
    )


# patrons INSERT


# patrons UPDATE


# patrons DELETE

# -----------CHECKOUTS-----------
# 6. checkouts.html
@app.route("/checkouts.html", methods=["POST", "GET"])
def checkouts_page():
    # Initial Display:
    query = """ 
    select
        Checkouts.checkout_id,
        Patrons.patron_first,  
        Patrons.patron_last,
        Checkouts.checkout_date,
        Checkouts.return_date
    from Patrons
        inner join Checkouts on Patrons.patron_id = Checkouts.patron_id
    order by Checkouts.checkout_date desc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    checkouts_headings = [
        "Checkout ID",
        "First Name",
        "Last Name",
        "Checkout Date",
        "Return Date",
    ]

    # Get Valid Patron Dropdown
    query2 = """SELECT patron_id, concat(patron_first, ' ', patron_last) as patron_name FROM Patrons ORDER BY patron_last ASC"""
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    results2 = cursor2.fetchall()
    print(results2)

    # checkout INSERT
    if request.method == "POST":
        request.form.get("insert Checkouts")
        input_patron = request.form["patron_choice"]
        input_checkout_date = request.form["checkout_date_input"]
        input_return_date = request.form["return_date_input"]
        query = f"""INSERT INTO Checkouts (checkout_date, return_date, patron_id) VALUES (%s, %s, %s) ; """
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(input_checkout_date, input_return_date, input_patron),
        )
        return redirect("/checkouts.html")

    return render_template(
        "table_template.j2",
        title="Checkouts",
        description="This is a database of checkouts. To select a checkout, click on the Checkout ID. From there, you can edit the checkout items.",
        headings=checkouts_headings,
        data=results,
        name_dropdown=results2,
        routeURL="checkout",
    )


# checkouts UPDATE

# checkouts DELETE
@app.route("/delete_checkout/<int:id>", methods=["GET", "POST"])
def delete_checkout(id):
    query = "DELETE FROM Checkouts WHERE checkout_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect("/checkouts.html")


# 6.1 - To CheckedBooks from Checkouts (Jenna)
@app.route("/checkedbooks/<checkout_id>")
def go_to_checkedbooks(checkout_id):
    checkedbooks_headings = [
        "Book Title",
        "Patron Name",
        "Checkout Date",
        "Return Date",
        "Returned",
    ]
    checkedbooks = []
    if checkout_id == "1":
        checkedbooks = [
            [
                "Sense and Sensibility",
                "Zelenka Fichter",
                "2022-02-03",
                "2022-02-24",
                "Yes",
            ],
            ["If It Bleeds", "Zelenka Fichter", "2022-02-03", "2022-02-24", "Yes"],
            ["Crooked House", "Zelenka Fichter", "2022-02-03", "2022-02-24", "Yes"],
        ]
    elif checkout_id == "2":
        checkedbooks = [
            ["A Farewell to Arms", "Zelenka Fichter", "2021-01-11", "2021-02-01", "Yes"]
        ]
    elif checkout_id == "3":
        checkedbooks = [
            [
                "Adventures of Huckleberry Finn",
                "Eloise Westfall",
                "2021-05-26",
                "2021-06-16",
                "Yes",
            ],
            [
                "The Adventures of Tom Sawyer: Original Illustrations",
                "Eloise Westfall",
                "2021-05-26",
                "2021-06-16",
                "Yes",
            ],
        ]
    elif checkout_id == "4":
        checkedbooks = [
            [
                "Adventures of Huckleberry Finn",
                "Corbett Farner",
                "2022-01-29",
                "2022-02-19",
                "Yes",
            ]
        ]
    elif checkout_id == "5":
        checkedbooks = [
            [
                "The Adventures of Tom Sawyer: Original Illustrations",
                "Koko Irish",
                "2021-10-29",
                "2021-11-19",
                "Yes",
            ],
            ["Needful Things", "Koko Irish", "2021-10-29", "2021-11-19", "Yes"],
            ["Sense and Sensibility", "Koko Irish", "2021-10-29", "2021-11-19", "Yes"],
        ]

    return render_template(
        "table_template.j2",
        title=f"Checkout #{checkout_id}",
        headings=checkedbooks_headings,
        data=checkedbooks,
        description="",
    )


# -----------CHECKEDBOOKS-----------
# 7. checkedbooks.html
@app.route("/checkedbooks.html")
def checkedbooks_page():
    query = """ 
    select Books.title,
        Patrons.patron_first,
        Patrons.patron_last,
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
        "Book Title",
        "Patron First",
        "Patron Last",
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

# -----------PUBLISHERS-----------
# 8. publishers.html
@app.route("/publishers.html")
def publishers_page():
    query = """ 
    select Publishers.publisher_name
    from Publishers
    order by Publishers.publisher_name asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    publishers_headings = ["Publisher Name"]
    return render_template(
        "table_template.j2",
        title="Book Publishers",
        description="This is a database of publishers",
        headings=publishers_headings,
        data=results,
    )


# publishers INSERT


# publishers UPDATE


# publishers DELETE

# -----------LOCATIONS-----------
# 9. locations.html
@app.route("/locations.html", methods=["POST", "GET"])
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
        description="This is a database of library locations",
        headings=locations_headings,
        data=results,
        routeURL="location",
    )


# locations UPDATE
@app.route("/update_location/<int:id>", methods=["POST", "GET"])
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
    )


# locations DELETE
@app.route("/delete_location/<int:id>", methods=["GET", "POST"])
def delete_location(id):
    query = "DELETE FROM Locations WHERE location_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect("/locations.html")


# Listener
# Port is 5000
if __name__ == "__main__":
    # #port = int(os.environ.get("PORT", 9112))
    # #                                ^^^^
    # #              You can replace this number with any valid port
    app.run()
