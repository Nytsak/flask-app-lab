from flask import render_template, redirect, url_for

from . import products_bp

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 25000,
        "description": "Powerful laptop for work and study"
    },
    {
        "id": 2,
        "name": "Smartphone",
        "price": 15000,
        "description": "Modern smartphone with large screen"
    },
    {
        "id": 3,
        "name": "Headphones",
        "price": 3000,
        "description": "Wireless headphones with noise cancellation"
    }
]


@products_bp.route("/")
def product_list():
    return render_template("products/list.html", products=products)


@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = products[product_id - 1]
    if not product:
        return redirect(url_for("products_bp.product_list"))
    return render_template("products/detail.html", product=product)
