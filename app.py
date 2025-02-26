from flask import Flask, send_from_directory, render_template
from flask_cors import CORS
from db_profile import conn
from flask_smorest import Api
from api import blp
import pymysql.cursors

app = Flask(__name__)
CORS(app)

# OpenAPI 관련 설정
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(blp)


@app.route("/")
def kream_items():
    conn.ping(reconnect=True)
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM kream k JOIN category c ON k.category = c.category_id LIMIT 10"
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


@app.route("/<path:name>", methods=["GET"])
def get_data(name):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(
            "SELECT * FROM kream k JOIN category c ON k.category = c.category_id WHERE product_name LIKE %s LIMIT 10;",
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


@app.route("/img/<path:filename>")
def get_image(filename):
    return send_from_directory("static/img", filename)


@app.route("/js/<path:filename>")
def get_js(filename):
    return send_from_directory("static/js", filename)


@app.route("/css/<path:filename>")
def get_css(filename):
    return send_from_directory("static/css", filename)


if __name__ == "__main__":
    app.run(debug=True)
