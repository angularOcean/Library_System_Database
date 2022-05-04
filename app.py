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


# Configuration

app = Flask(__name__)

# Routes
@app.route("/")
def index():
    return render_template("main.j2")


# 1. index.html
# render a navigation bar
@app.route("/index.html")
def root():
    return render_template("main.j2")


# 2. authors.html - Jenna
@app.route("/authors.html")
def authors_page():
    return render_template(
        "table_template.j2",
        title="Authors",
        headings=authors_headings,
        data=authors_data,
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
        title ="Books",
        headings =books_headings, 
        data= books_rows)


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
    )


book_copies_headings = ["Title", "Author", "Location"]

book_copies_rows = [
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


# 5. patrons.html - Herakles
@app.route("/patrons.html")
def patrons_page():
    return render_template(
        "table_template.j2", 
        title = "Patrons",
        headings=patrons_headings,
        data = patrons_rows
        )

patrons_headings = ["First Name", "Last Name", "Email"]
patrons_rows = [
    ["Koko",  "Irish", "kokoiri@egl.com"],
    ["Corbett", "Farner",  "corbetfarn@gmail.com"],
    ["Eloise",  "Westfall", "elwestfa@hotmail.com"],
]

# 6. checkouts.html - Jenna
@app.route("/checkouts.html")
def checkouts_page():
    return render_template(
        "table_template.j2",
        title="Checkouts",
        description="They are sorted by the most recent checkout date.",
        headings=checkouts_headings,
        data=checkouts_rows,
    )


checkouts_headings = ["Patron Name", "Checkout Date", "Return Date"]
checkouts_rows = [
    ["Zelenka Fichter", "2022-02-03", "2022-02-24"],
    ["Corbett Farner", "2022-01-29", "2022-02-19"],
    ["Koko Irish", "2021-10-29", "2021-11-19"],
    ["Eloise Westfall", "2021-05-26", "2021-06-16"],
    ["Zelenka Fichter", "2021-01-11", "2021-02-01"],
]

# 7. checkedbooks.html - Herakles
@app.route("/checkedbooks.html")
def checkedbooks_page():
    return render_template("table_template.j2",
        title = "Checked Books", 
        headings=checkedbooks_headings,
        data = checkedbooks_rows
        )

checkedbooks_headings = ["Book_Title","Patron_Name", "Checkout_Date", "Return_Date", "Returned"]
checkedbooks_rows= [
    [
        "Sense and Sensibility",
        "Zelenka Fichter",
        "2022-02-03",
        "2022-02-24",
        "Yes",
    ],
    [
        "Pride and Prejudice",
        "Koko Irish",
         "2021-10-29",
        "2021-11-19",
        "Yes",
    ],
    [
        "Crooked House",
        "Blanche Estell",
         "2021-01-11",
        "2021-02-01",
        "Yes",
    ],
]
# 8. publishers.html - Jenna
@app.route("/publishers.html")
def publishers_page():
    return render_template(
        "table_template.j2",
        title="Book Publishers",
        headings=publisher_headings,
        data=publisher_rows,
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
        title = "Locations",
        headings=locations_headings,
        data = locations_rows
        )


locations_headings = ["Name", "Address"]
locations_rows = [
    ["Little Penguin Library", "67 Cooper Ave"],
    [ "Macaroni Penguin Library",  "658 Lincoln Lane"],
    ["Emperor Penguin Library",  "7580 Devon Rd"],
    ["Rockhopper Penguin Library",  "319 6th St"],
    ["Royal Penguin Library", "309 East Walnutwood Lane"],
]

# Listener

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9112))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
