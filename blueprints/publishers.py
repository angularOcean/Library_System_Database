# Publishers Page: Select, Insert, Update, Delete

from flask import Blueprint, Flask, render_template, request, redirect, g
import database.db_connector as db
import app

publishers_bp = Blueprint("publishers", __name__)

# -----------PUBLISHERS-----------
# publishers.html
@publishers_bp.route("/publishers.html", methods=["POST", "GET"])
def publishers_page():
    query = """ 
    select publisher_id,
    publisher_name
    from Publishers
    order by Publishers.publisher_name asc;
    """
    cursor = db.execute_query(db_connection=app.db_connection, query=query)
    results = cursor.fetchall()
    publishers_headings = ["ID", "Publisher Name"]

    # publishers INSERT
    if request.method == "POST":
        request.form.get("insert Publishers")
        publisher_name = request.form["Publisher Name"]
        query = f"INSERT INTO Publishers(publisher_name) VALUES (%s); "
        cursor = db.execute_query(
            db_connection=app.db_connection,
            query=query,
            query_params=(publisher_name,),
        )
        return redirect("/publishers.html")

    return render_template(
        "table_template.j2",
        title="Book Publishers",
        description="This is the publisher data for the Penguin Library System.",
        headings=publishers_headings,
        data=results,
        routeURL="publisher",
    )


# publishers UPDATE
@publishers_bp.route("/update_publisher/<int:id>", methods=["POST", "GET"])
def publishers_edit(id):
    if request.method == "GET":
        query = "SELECT publisher_name FROM Publishers WHERE publisher_id = %s"
        curr = db.execute_query(
            db_connection=app.db_connection, query=query, query_params=(id,)
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
            db_connection=app.db_connection,
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
@publishers_bp.route("/delete_publisher/<int:id>", methods=["GET", "POST"])
def delete_publisher(id):
    query = "DELETE FROM Publishers WHERE publisher_id = %s"
    curr = db.execute_query(
        db_connection=app.db_connection, query=query, query_params=(id,)
    )
    return redirect("/publishers.html")
