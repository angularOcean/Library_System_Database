# ------- Citations ---------

# Citation for table_template:
# Date: 05/03/2022
# Based on:
# Source URL: https://www.youtube.com/watch?v=mCy52I4exTU

# Citation for app.py:
# Date: 05/03/2022
# Based on: OSU CS340 Flask Starter Guide
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, request, redirect
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


# -----------HOME PAGE-----------
@app.route("/")
def index():
    return render_template("home_template.j2")


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
        query = "INSERT INTO Authors(author_first, author_last) VALUES (%s,%s); "
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
        query = "UPDATE Authors SET author_first = %s, author_last = %s WHERE author_id = %s;"
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
        routeURL="authors",
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
@app.route("/books.html", methods=["POST", "GET"])
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
@app.route("/update_book/<int:id>", methods=["GET", "POST"])
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
@app.route("/delete_book/<int:id>", methods=["GET", "POST"])
def delete_book(id):
    query = "DELETE FROM Books WHERE book_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect("/books.html")


# -----------BOOKCOPIES-----------

# 4. bookcopies.html
@app.route("/bookcopies.html")
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


# 4.1 Dynamically Display Checked Out Books
@app.route("/bookcopies/checked-out")
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


# 4.2 Dynamically Display Returned Books (On Shelf)
@app.route("/bookcopies/on-shelf")
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


# bookcopies DELETE


# -----------PATRONS-----------
# 5. patrons.html - Herakles
@app.route("/patrons.html", methods=["POST", "GET"])
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
@app.route("/update_patron/<int:id>", methods=["POST", "GET"])
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
@app.route("/delete_patron/<int:id>", methods=["GET", "POST"])
def delete_patron(id):
    query = "DELETE FROM Patrons WHERE patron_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect("/patrons.html")


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
    order by Checkouts.checkout_id asc;
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
    query2 = """SELECT patron_id, concat(patron_first, ' ', patron_last) as patron_name FROM Patrons ORDER BY patron_last ASC;"""
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    results2 = cursor2.fetchall()

    # checkout INSERT
    if request.method == "POST":
        request.form.get("insert Checkouts")
        input_patron = request.form["patron_choice"]
        input_checkout_date = request.form["checkout_date_input"]
        input_return_date = request.form["return_date_input"]
        query = """INSERT INTO Checkouts (checkout_date, return_date, patron_id) VALUES (%s, %s, %s) ; """
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(input_checkout_date, input_return_date, input_patron),
        )
        return redirect("/checkouts.html")

    return render_template(
        "table_template.j2",
        title="Checkouts",
        description="This is a database of checkouts. To select a checkout, click on the Checkout ID. This will display the CheckedBooks table for that Checkout ID. On that page, you can add, update, and delete the patron's checkout items.",
        headings=checkouts_headings,
        data=results,
        name_dropdown=results2,
        routeURL="checkout",
    )


# checkouts UPDATE
@app.route("/update_checkout/<int:id>", methods=["GET", "POST"])
def checkouts_edit(id):
    if request.method == "GET":
        query = """
        SELECT Checkouts.checkout_id, Patrons.patron_id, Patrons.patron_first, Patrons.patron_last, Checkouts.checkout_date, Checkouts.return_date 
        FROM Patrons 
        INNER JOIN Checkouts ON Patrons.patron_id = Checkouts.patron_id 
        WHERE checkout_id = %s"""
        curr = db.execute_query(
            db_connection=db_connection, query=query, query_params=(id,)
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
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    results2 = cursor2.fetchall()

    if request.method == "POST":
        request.form.get("Update Checkout")
        patron_choice = request.form["patron_choice"]
        checkout_date_input = request.form["checkout_date_input"]
        return_date_input = request.form["return_date_input"]
        checkout_id = id
        query = "UPDATE Checkouts SET patron_id = %s, checkout_date=%s, return_date=%s WHERE checkout_id=%s"
        curr = db.execute_query(
            db_connection=db_connection,
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
    # Initial Display:
    query = """
    SELECT BookCopies.copy_id, Books.title, Locations.location_name, Checkouts.checkout_date, Checkouts.return_date, CheckedBooks.returned
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
        "Copy ID",
        "Book Title",
        "Copy Location",
        "Checkout Date",
        "Return Date",
        "Returned",
    ]

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

    return render_template(
        "table_template.j2",
        title=f"Checkout #{checkout_id}",
        headings=checkedbooks_headings,
        data=info,
        description=f"For Patron: {info2[0]}",
        checkout_id=checkout_id,
        routeURL="checkedbook",
    )


# -----------CHECKEDBOOKS-----------
# 7. checkedbooks.html
@app.route("/checkedbooks.html")
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

# -----------PUBLISHERS-----------
# 8. publishers.html
@app.route("/publishers.html", methods=["POST", "GET"])
def publishers_page():
    query = """ 
    select publisher_id,
    publisher_name
    from Publishers
    order by Publishers.publisher_name asc;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    publishers_headings = ["ID", "Publisher Name"]

    # publishers INSERT
    if request.method == "POST":
        request.form.get("insert Publishers")
        publisher_name = request.form["Publisher Name"]
        query = f"INSERT INTO Publishers(publisher_name) VALUES (%s); "
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(publisher_name,),
        )
        return redirect("/publishers.html")

    return render_template(
        "table_template.j2",
        title="Book Publishers",
        description="This is a database of publishers",
        headings=publishers_headings,
        data=results,
        routeURL="publisher",
    )


# publishers UPDATE
@app.route("/update_publisher/<int:id>", methods=["POST", "GET"])
def publishers_edit(id):
    if request.method == "GET":
        query = "SELECT publisher_name FROM Publishers WHERE publisher_id = %s"
        curr = db.execute_query(
            db_connection=db_connection, query=query, query_params=(id,)
        )
        info = curr.fetchall()
        print(info)

    publishers_edit_headings = ["Publisher Name"]

    if request.method == "POST":
        request.form.get("Update Publisher")
        publisher_name = request.form["Publisher Name"]
        publisher_id = id
        query = f"update Publishers set publisher_name = %s where publisher_id = %s;"
        curr = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(publisher_name, publisher_id),
        )
        return redirect("/publishers.html")

    return render_template(
        "update_template.j2",
        data=info,
        description="Editing Publisher: ",
        headings=publishers_edit_headings,
        title="Publisher",
        routeURL="publishers",
    )


# publishers DELETE
@app.route("/delete_publisher/<int:id>", methods=["GET", "POST"])
def delete_publisher(id):
    query = "DELETE FROM Publishers WHERE publisher_id = %s"
    curr = db.execute_query(
        db_connection=db_connection, query=query, query_params=(id,)
    )
    return redirect("/publishers.html")


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
        routeURL="locations",
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
