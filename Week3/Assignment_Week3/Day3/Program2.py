# 2. Product Inventory CRUD API.
from flask import Flask, request, jsonify

app = Flask(__name__)

products = []


# CREATE
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    products.append(data)

    return jsonify({"message": "Product Added"}), 201


# READ
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


# READ ONE
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):

    for product in products:

        if product["id"] == id:
            return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


# UPDATE
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):

    data = request.get_json()

    for product in products:

        if product["id"] == id:

            product["name"] = data["name"]
            product["price"] = data["price"]
            product["quantity"] = data["quantity"]

            return jsonify({"message": "Updated"})

    return jsonify({"error": "Product not found"}), 404


# DELETE
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):

    for product in products:

        if product["id"] == id:
            products.remove(product)
            return jsonify({"message": "Deleted"})

    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)