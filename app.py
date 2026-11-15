from flask import Flask, render_template, request

from db import LOCATIONS, QUANTITIES, close_db, get_db, init_db
from qr import qr_bp, qr_public_bp
from reagents import reagents_bp

app = Flask(__name__)
app.teardown_appcontext(close_db)

app.register_blueprint(reagents_bp)
app.register_blueprint(qr_bp)
app.register_blueprint(qr_public_bp)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword", "").strip()
    location = request.args.get("location", "").strip()
    quantity = request.args.get("quantity", "").strip()

    sql = "SELECT * FROM supplies WHERE 1 = 1"
    params = []

    if keyword:
        sql += " AND (name LIKE ? OR category LIKE ? OR description LIKE ?)"
        like_keyword = f"%{keyword}%"
        params.extend([like_keyword, like_keyword, like_keyword])

    if location:
        sql += " AND location = ?"
        params.append(location)

    if quantity:
        sql += " AND quantity = ?"
        params.append(quantity)

    sql += " ORDER BY cabinet_number, name"

    supplies = get_db().execute(sql, params).fetchall()

    return render_template(
        "search.html",
        supplies=supplies,
        keyword=keyword,
        location=location,
        quantity=quantity,
        locations=LOCATIONS,
        quantities=QUANTITIES,
    )


@app.route("/supply/<int:supply_id>")
def supply_detail(supply_id):
    supply = get_db().execute(
        "SELECT * FROM supplies WHERE id = ?", (supply_id,)
    ).fetchone()

    if supply is None:
        return render_template("not_found.html"), 404

    return render_template("detail.html", supply=supply)


@app.route("/location")
def location():
    selected_lab = request.args.get("lab", "").strip()
    cabinets = []

    # 보일랩을 선택한 뒤에만 1번부터 6번 시약장을 보여 준다.
    if selected_lab in LOCATIONS:
        db = get_db()
        for number in range(1, 7):
            items = db.execute(
                """
                SELECT * FROM supplies
                WHERE location = ? AND cabinet_number = ?
                ORDER BY name
                """,
                (selected_lab, number),
            ).fetchall()
            cabinets.append({"number": number, "supplies": items})

    return render_template(
        "location.html",
        locations=LOCATIONS,
        selected_lab=selected_lab,
        cabinets=cabinets,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
