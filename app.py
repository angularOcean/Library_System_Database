from flask import Flask, render_template
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
    pass


# 3. books.html - Herakles
@app.route("/books.html")
def books_page():
    return render_template("books.j2", books=books_from_app_py)


books_from_app_py = [
    {
        "ISBN": "978-19-8213798-4 ",
        "Title": "If It Bleeds",
        "Year": 2021,
        "Author": "Stephen King",
        "Publisher": "Scribner",
    },
    {
        "ISBN": "978-15-0114741-8",
        "Title": "Needful Things",
        "Year": 2018,
        "Author": "Stephen King",
        "Publisher": "Gallery Books",
    },
    {
        "ISBN": "978-1948-13282-4",
        "Title": "The Adventures of Tom Sawyer: Original Illustrations",
        "Year": "2018",
        "Author": "Mark Twain",
        "Publisher": "SeeWolf Books",
    },
    {
        "ISBN": "978-0062-07348-8",
        "Title": "And Then There Were None",
        "Year": "2011",
        "Author": "Agatha Christie",
        "Publisher": "Dover Publications",
    },
]

# 4. bookcopies.html - Jenna
@app.route("/bookcopies.html")
def bookcopies_page():
    pass


# 5. patrons.html - Herakles
@app.route("/patrons.html")
def patrons_page():
    return render_template("patrons.j2", patrons=patrons_from_app_py)


patrons_from_app_py = [
    {"First_Name": "Koko", "Last_Name": "Irish", "Email": "kokoiri@egl.com"},
    {"First_Name": "Corbett", "Last_Name": "Farner", "Email": "corbetfarn@gmail.com"},
    {"First_Name": "Eloise", "Last_Name": "Westfall", "Email": "elwestfa@hotmail.com"},
]

# 6. checkouts.html - Jenna
@app.route("/checkouts.html")
def checkouts_page():
    pass


# 7. checkedbooks.html - Herakles
@app.route("/checkedbooks.html")
def checkedbooks_page():
    return render_template("checkedbooks.j2", checkedbooks=checkedbooks_from_app_py)


checkedbooks_from_app_py = [
    {
        "Book_Title": "Sense and Sensibility",
        "Patron_Name": "Zelenka Fichter",
        "Checkout_Date": "2022-02-03",
        "Return_Date": "2022-02-24",
        "Returned": "Yes",
    },
    {
        "Book_Title": "Pride and Prejudice",
        "Patron_Name": "Koko Irish",
        "Checkout_Date": "2021-10-29",
        "Return_Date": "2021-11-19",
        "Returned": "Yes",
    },
    {
        "Book_Title": "Crooked House",
        "Patron_Name": "Blanche Estell",
        "Checkout_Date": "2021-01-11",
        "Return_Date": "2021-02-01",
        "Returned": "Yes",
    },
]
# 8. publishers.html - Jenna
@app.route("/publishers.html")
def publishers_page():
    pass


# 9. locations.html - Herakles
@app.route("/locations.html")
def locations_page():
    return render_template("locations.j2", locations=locations_from_app_py)


locations_from_app_py = [
    {"Name": "Little Penguin Library", "Address": "67 Cooper Ave"},
    {"Name": "Macaroni Penguin Library", "Address": "658 Lincoln Lane"},
    {"Name": "Emperor Penguin Library", "Address": "7580 Devon Rd"},
    {"Name": "Rockhopper Penguin Library", "Address": "319 6th St"},
    {"Name": "Royal Penguin Library", "Address": "309 East Walnutwood Lane"},
]

# Listener

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9112))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
