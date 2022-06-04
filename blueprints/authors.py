# Authors Page: Select, Insert, Update, Delete

from flask import Blueprint, Flask, render_template, request, redirect, g
import database.db_connector as db
import app
from config import DevelopmentConfig, ProductionConfig
from os import environ
from dotenv import load_dotenv, find_dotenv

# Load the .env file into the environment variables
load_dotenv(find_dotenv())

authors_bp = Blueprint("authors", __name__)

# -----------AUTHORS-----------
# authors.html
@authors_bp.route("/authors.html", methods=["POST", "GET"])
def authors_page():
    # Initial Display:
    query = "select author_id, author_first, author_last from Authors order by author_last asc;"
    cursor = db.execute_query(db_connection=app.db_connection, query=query)
    results = cursor.fetchall()
    authors_headings = ["ID", "First Name", "Last Name"]

    # author INSERT
    if request.method == "POST":
        request.form.get("insert Authors")
        author_fname = request.form["First Name"]
        author_lname = request.form["Last Name"]
        query = "INSERT INTO Authors(author_first, author_last) VALUES (%s,%s); "
        cursor = db.execute_query(
            db_connection=app.db_connection,
            query=query,
            query_params=(author_fname, author_lname),
        )
        return redirect("/authors.html")

    return render_template(
        "table_template.j2",
        title="Authors",
        description="This is the author data for the Penguin Library System.",
        headings=authors_headings,
        routeURL="author",
        data=results,
    )


# author UPDATE
@authors_bp.route("/update_author/<int:id>", methods=["POST", "GET"])
def authors_edit(id):
    if request.method == "GET":
        query = "SELECT author_id, author_first, author_last FROM Authors WHERE author_id = %s"
        curr = db.execute_query(
            db_connection=app.db_connection, query=query, query_params=(id,)
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
            db_connection=app.db_connection,
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
@authors_bp.route("/delete_author/<int:id>", methods=["GET", "POST"])
def delete_author(id):
    query = "DELETE FROM Authors WHERE author_id = %s"
    curr = db.execute_query(
        db_connection=app.db_connection, query=query, query_params=(id,)
    )
    return redirect("/authors.html")
