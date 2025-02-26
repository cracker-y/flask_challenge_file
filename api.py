from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db_profile import conn
import pymysql.cursors
from flask import render_template, send_from_directory
from flask_cors import CORS

blp = Blueprint(
    "search", "search", url_prefix="/search", description="Operations on items"
)


@blp.route("/", methods=["GET"])
def signup(name):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM kream k JOIN category c ON k.category = c.category_id WHERE product_name LIKE %s;",
            f"%{name}%",
        )
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
