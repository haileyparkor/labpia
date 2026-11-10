
from flask import Flask, render_template, request, g
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "inventory.db")

app = Flask(__name__)

REMAINING_LEVELS = ["많음", "보통", "적음", "없음"]

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    db = get_db()
    locations = db.execute("SELECT * FROM locations ORDER BY id").fetchall()
    recent_items = db.execute(
        "SELECT * FROM items ORDER BY updated_at DESC LIMIT 6"
    ).fetchall()
    return render_template("home.html", locations=locations, recent_items=recent_items)

@app.route("/items")
def item_list():
    query = request.args.get("q", "").strip()
    location_id = request.args.get("location_id", type=int)
    remaining = request.args.get("remaining", "").strip()

    sql = """
        SELECT items.*, locations.name AS location_name
        FROM items
        JOIN locations ON items.location_id = locations.id
        WHERE 1=1
    """
    params = []

    if query:
        sql += " AND (items.name LIKE ? OR items.category LIKE ? OR items.description LIKE ?)"
        params += [f"%{query}%"] * 3

    if location_id:
        sql += " AND items.location_id = ?"
        params.append(location_id)

    if remaining in REMAINING_LEVELS:
        sql += " AND items.remaining_level = ?"
        params.append(remaining)

    sql += " ORDER BY items.name"

    db = get_db()
    items = db.execute(sql, params).fetchall()
    locations = db.execute("SELECT * FROM locations ORDER BY id").fetchall()

    return render_template(
        "item_list.html",
        items=items,
        locations=locations,
        query=query,
        selected_location_id=location_id,
        selected_remaining=remaining,
        remaining_levels=REMAINING_LEVELS,
    )

@app.route("/items/<int:item_id>")
def item_detail(item_id):
    db = get_db()
    item = db.execute(
        """
        SELECT items.*, locations.name AS location_name
        FROM items
        JOIN locations ON items.location_id = locations.id
        WHERE items.id = ?
        """,
        (item_id,),
    ).fetchone()

    if item is None:
        return render_template("not_found.html"), 404

    return render_template("item_detail.html", item=item)

@app.route("/map")
def map_page():
    db = get_db()
    locations = db.execute("SELECT * FROM locations ORDER BY id").fetchall()
    selected_location_id = request.args.get("location_id", type=int)

    items = []
    selected_location = None

    if selected_location_id:
        selected_location = db.execute(
            "SELECT * FROM locations WHERE id = ?", (selected_location_id,)
        ).fetchone()
        items = db.execute(
            """
            SELECT * FROM items
            WHERE location_id = ?
            ORDER BY cabinet_number, name
            """,
            (selected_location_id,),
        ).fetchall()

    return render_template(
        "map.html",
        locations=locations,
        selected_location=selected_location,
        selected_location_id=selected_location_id,
        items=items,
    )

if __name__ == "__main__":
    app.run(debug=True)
