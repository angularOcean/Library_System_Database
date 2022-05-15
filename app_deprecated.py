# ------- Citations ---------

# Citation for table_template:
# Date: 05/03/2022
# Based on:
# Source URL: https://www.youtube.com/watch?v=mCy52I4exTU

# Citation for app.py:
# Date: 05/03/2022
# Based on: OSU CS340 Flask Starter Guide
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, json
import os
import pymysql
from flask import request
import database.db_connector as db
from boto.s3.connection import S3Connection


# Configuration

app = Flask(__name__)

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_CURSORCLASS"] = os.environ.get("MYSQL_CURSORCLASS")

# Connect to Database
db_connection = db.connect_to_database()

# Routes
@app.route("/")
def index():
    return render_template("main.j2")


# SAMPLE TO TEST DB CONNECTION
@app.route("/sample.html")
def sample():
    query = "SELECT * FROM Patrons;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    patrons_headings = ["ID", "First Name", "Last Name", "Email"]
    return render_template(
        "table_template.j2", title="Patrons", headings=patrons_headings, data=results
    )


# 1. index.html
# render a navigation bar
@app.route("/index.html")
def root():
    return render_template("main.j2")


#authors.html
@app.route("/authors.html")
def authors_page():
    query = "select author_first, author_last from Authors order by author_last asc;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    authors_headings = [ "First Name", "Last Name"]
    return render_template(
        "table_template.j2", title="Authors", headings=authors_headings, data=results
    )

# 2. authors.html - Jenna
@app.route("/authors2.html")
def authors_page2():
    return render_template(
        "table_template.j2",
        title="Authors",
        headings=authors_headings,
        data=authors_data,
        description="",
    )


authors_headings = ["First Name", "Last Name"]
authors_data = [
    ["Stephen", "King"],
    ["Mark", "Twain"],
    ["Agatha", "Christie"],
    ["Jane", "Austen"],
    ["Ernest", "Hemingway"],
]

# 3. books.html - Herakles
@app.route("/books.html")
def books_page():
    return render_template(
        "table_template.j2",
        title="Books",
        headings=books_headings,
        data=books_rows,
        description="",
    )


books_headings = ["ISBN", "Title", "Year", "Author", "Publisher"]
books_rows = [
    [
        "978-19-8213798-4 ",
        "If It Bleeds",
        2021,
        "Stephen King",
        "Scribner",
    ],
    [
        "978-15-0114741-8",
        "Needful Things",
        2018,
        "Stephen King",
        "Gallery Books",
    ],
    [
        "978-1948-13282-4",
        "The Adventures of Tom Sawyer: Original Illustrations",
        2018,
        "Mark Twain",
        "SeeWolf Books",
    ],
    [
        "978-0062-07348-8",
        "And Then There Were None",
        2011,
        "Agatha Christie",
        "Dover Publications",
    ],
]

# 4. bookcopies.html - Jenna
@app.route("/bookcopies.html")
def bookcopies_page():
    return render_template(
        "table_template.j2",
        title="Book Copies",
        headings=book_copies_headings,
        data=book_copies_rows,
        description="",
    )


book_copies_headings = ["Title", "Author", "Location"]

book_copies_rows = [
    ["Charlie and the Chocolate Factory", "Roald Dahl", "Royal Penguin Library"],
    ["A Farewell to Arms", "Ernest Hemingway", "Little Penguin Library"],
    ["A Farewell to Arms", "Ernest Hemingway", "Macaroni Penguin Library"],
    ["Adventures of Huckleberry Finn", "Mark Twain", "Royal Penguin Library"],
    ["And Then There Were None", "Agatha Christie", "Macaroni Penguin Library"],
    ["Crooked House", "Agatha Christie", "Rockhopper Penguin Library"],
    ["Crooked House", "Agatha Christie", "Emperor Penguin Library"],
    ["For Whom the Bell Tolls", "Ernest Hemingway", "Emperor Penguin Library"],
    ["If It Bleeds", "Stephen King", "Rockhopper Penguin Library"],
    ["If It Bleeds", "Stephen King", "Royal Penguin Library"],
    ["Needful Things", "Stephen King", "Emperor Penguin Library"],
    ["Pride and Prejudice", "Jane Austen", "Rockhopper Penguin Library"],
    ["Sense and Sensibility", "Jane Austen", "Royal Penguin Library"],
    [
        "The Adventures of Tom Sawyer: Original Illustrations",
        "Mark Twain",
        "Little Penguin Library",
    ],
    [
        "The Adventures of Tom Sawyer: Original Illustrations",
        "Mark Twain",
        "Macaroni Penguin Library",
    ],
]

# 4.1 Dynamically Display Checked Out Books
@app.route("/bookcopies/checked-out")
def show_checked_out():
    checked_out_headings = ["Title", "Author", "Location", "Return Date"]
    checked_out_sample = [
        [
            "Charlie and the Chocolate Factory",
            "Roald Dahl",
            "Royal Penguin Library",
            "2022-06-11",
        ]
    ]
    return render_template(
        "table_template.j2",
        title="Checked Out Books",
        headings=checked_out_headings,
        data=checked_out_sample,
    )


# 4.2 Dynamically Display Returned Books (On Shelf)
@app.route("/bookcopies/on-shelf")
def show_on_shelf():
    return render_template(
        "table_template.j2",
        title="Books on the Shelf",
        headings=book_copies_headings,
        data=book_copies_rows,
    )


# 5. patrons.html - Herakles
@app.route("/patrons.html")
def patrons_page():
    return render_template(
        "table_template.j2",
        title="Patrons",
        headings=patrons_headings,
        data=patrons_rows,
        description="",
    )


patrons_headings = ["First Name", "Last Name", "Email"]
patrons_rows = [
    ["Koko", "Irish", "kokoiri@egl.com"],
    ["Corbett", "Farner", "corbetfarn@gmail.com"],
    ["Eloise", "Westfall", "elwestfa@hotmail.com"],
]

# 6. checkouts.html - Jenna
@app.route("/checkouts.html")
def checkouts_page():
    return render_template(
        "table_template.j2",
        title="Checkouts",
        description="They are sorted by the most recent checkout date. Click on a Checkout ID to view the items in the checkout selected.",
        headings=checkouts_headings,
        data=checkouts_rows,
    )


checkouts_headings = ["Checkout ID", "Patron Name", "Checkout Date", "Return Date"]
checkouts_rows = [
    [1, "Zelenka Fichter", "2022-02-03", "2022-02-24"],
    [4, "Corbett Farner", "2022-01-29", "2022-02-19"],
    [5, "Koko Irish", "2021-10-29", "2021-11-19"],
    [3, "Eloise Westfall", "2021-05-26", "2021-06-16"],
    [2, "Zelenka Fichter", "2021-01-11", "2021-02-01"],
]

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


# 7. checkedbooks.html - Herakles
@app.route("/checkedbooks.html")
def checkedbooks_page():
    return render_template(
        "table_template.j2",
        title="Checked Books",
        headings=checkedbooks_headings,
        data=checkedbooks_rows,
        description="This is a read-only list of all checkout line items in the Penguin Library Database. Please edit any checkout information from the Checkouts page.",
    )


checkedbooks_headings = [
    "Book Title",
    "Patron Name",
    "Checkout Date",
    "Return Date",
    "Returned",
]
checkedbooks_rows = [
    ["Sense and Sensibility", "Zelenka Fichter", "2022-02-03", "2022-02-24", "Yes"],
    ["If It Bleeds", "Zelenka Fichter", "2022-02-03", "2022-02-24", "Yes"],
    ["Crooked House", "Zelenka Fichter", "2022-02-03", "2022-02-24", "Yes"],
    ["A Farewell to Arms", "Zelenka Fichter", "2021-01-11", "2021-02-01", "Yes"],
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
    [
        "Adventures of Huckleberry Finn",
        "Corbett Farner",
        "2022-01-29",
        "2022-02-19",
        "Yes",
    ],
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


# 8. publishers.html - Jenna
@app.route("/publishers.html")
def publishers_page():
    return render_template(
        "table_template.j2",
        title="Book Publishers",
        headings=publisher_headings,
        data=publisher_rows,
        description="",
    )


publisher_headings = ["Publisher Name"]
publisher_rows = [
    ["Dover Publications"],
    ["Forgotten Books"],
    ["Gallery Books"],
    ["Penguin Books"],
    ["Scribner"],
    ["SeeWolf Press"],
    ["William Morrow"],
]


# 9. locations.html - Herakles
@app.route("/locations.html")
def locations_page():
    return render_template(
        "table_template.j2",
        title="Locations",
        headings=locations_headings,
        data=locations_rows,
        description="",
    )


locations_headings = ["Name", "Address"]
locations_rows = [
    ["Little Penguin Library", "67 Cooper Ave"],
    ["Macaroni Penguin Library", "658 Lincoln Lane"],
    ["Emperor Penguin Library", "7580 Devon Rd"],
    ["Rockhopper Penguin Library", "319 6th St"],
    ["Royal Penguin Library", "309 East Walnutwood Lane"],
]

# Listener
# Port is 5000
if __name__ == "__main__":
    # #port = int(os.environ.get("PORT", 9112))
    # #                                ^^^^
    # #              You can replace this number with any valid port
    app.run(debug=True)