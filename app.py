from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from db_profile import conn
import pymysql.cursors

app = Flask(__name__)
CORS(app)


@app.route("/")
def kream_items():
    conn.ping(reconnect=True)
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM kream k JOIN category c ON k.category = c.category_id LIMIT 10")
        items = cursor.fetchall()

    products = [
        {
            "category": row.get("name"),
            "brand": row.get("brand"),
            "product_name": row.get("product_name"),
            "price": row.get("price"),
            # "img": str(row.get("img", "/statuc/image.png")).replace("https", "http"),
            # "item_img": row.get("img", "/statuc/image.png"),
            "item_img": row.get("statuc/image.png"),
        }
        for row in items
    ]
    return render_template("kream_items.html", data=products)

@app.route("/img/<path:filename>")
def get_image(filename):
    return send_from_directory("static/img", filename)


if __name__ == "__main__":
    app.run(debug=True)
