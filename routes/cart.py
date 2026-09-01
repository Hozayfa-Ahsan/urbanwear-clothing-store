from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

from models.product import Product


cart_bp = Blueprint(
    "cart",
    __name__
)


def get_cart():

    return session.get("cart", {})


def save_cart(cart):

    session["cart"] = cart
    session.modified = True


def build_cart_items():

    cart = get_cart()

    items = []
    subtotal = 0.0

    for product_id, item in cart.items():

        try:
            product_id = int(product_id)
        except (TypeError, ValueError):
            continue

        product = Product.query.get(product_id)

        if not product:
            continue

        try:
            quantity = int(
                item.get("quantity", 1)
            )
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        size = item.get(
            "size",
            ""
        )

        price = product.current_price()

        item_total = price * quantity

        subtotal += item_total

        items.append({
            "product": product,
            "quantity": quantity,
            "size": size,
            "price": price,
            "total": item_total
        })

    return items, subtotal


# =========================================================
# CART PAGE
# =========================================================

@cart_bp.route("/cart")
def cart():

    items, subtotal = build_cart_items()

    shipping = 0 if subtotal >= 75 else 8.99

    total = subtotal + shipping

    return render_template(
        "cart.html",
        items=items,
        subtotal=subtotal,
        shipping=shipping,
        total=total
    )


# =========================================================
# ADD TO CART
# =========================================================

@cart_bp.route(
    "/cart/add",
    methods=["POST"]
)
def add_to_cart():

    product_id = request.form.get(
        "product_id"
    )

    if not product_id:

        flash(
            "Product information is missing.",
            "error"
        )

        return redirect(
            request.referrer or
            url_for("cart.cart")
        )

    try:

        product_id = int(product_id)

    except (TypeError, ValueError):

        flash(
            "Invalid product.",
            "error"
        )

        return redirect(
            request.referrer or
            url_for("cart.cart")
        )


    product = Product.query.get_or_404(
        product_id
    )


    # -----------------------------------------------------
    # QUANTITY
    # -----------------------------------------------------

    try:

        quantity = int(
            request.form.get(
                "quantity",
                1
            )
        )

    except (TypeError, ValueError):

        quantity = 1


    if quantity < 1:

        quantity = 1


    if product.stock <= 0:

        flash(
            "This product is currently out of stock.",
            "error"
        )

        return redirect(
            request.referrer or
            url_for("cart.cart")
        )


    if quantity > product.stock:

        quantity = product.stock


    # -----------------------------------------------------
    # SIZE
    # -----------------------------------------------------

    size = request.form.get(
        "size",
        ""
    ).strip()


    # -----------------------------------------------------
    # CART
    # -----------------------------------------------------

    cart = get_cart()

    key = str(product.id)


    if key in cart:

        current_quantity = int(
            cart[key].get(
                "quantity",
                0
            )
        )

        new_quantity = (
            current_quantity +
            quantity
        )

        cart[key]["quantity"] = min(
            new_quantity,
            product.stock
        )

        if size:

            cart[key]["size"] = size


    else:

        cart[key] = {

            "quantity": quantity,

            "size": size

        }


    save_cart(cart)


    flash(
        f"{product.name} added to your cart.",
        "success"
    )


    return redirect(
        request.referrer or
        url_for("cart.cart")
    )


# =========================================================
# UPDATE CART
# =========================================================

@cart_bp.route(
    "/cart/update",
    methods=["POST"]
)
def update_cart():

    product_id = request.form.get(
        "product_id"
    )


    try:

        product_id = int(product_id)

    except (TypeError, ValueError):

        return redirect(
            url_for("cart.cart")
        )


    try:

        quantity = int(
            request.form.get(
                "quantity",
                1
            )
        )

    except (TypeError, ValueError):

        quantity = 1


    product = Product.query.get_or_404(
        product_id
    )


    cart = get_cart()

    key = str(product.id)


    if key not in cart:

        return redirect(
            url_for("cart.cart")
        )


    if quantity <= 0:

        cart.pop(key)

    else:

        cart[key]["quantity"] = min(
            quantity,
            product.stock
        )


    save_cart(cart)


    return redirect(
        url_for("cart.cart")
    )


# =========================================================
# REMOVE FROM CART
# =========================================================

@cart_bp.route(
    "/cart/remove",
    methods=["POST"]
)
def remove_from_cart():

    product_id = request.form.get(
        "product_id"
    )


    cart = get_cart()


    cart.pop(
        str(product_id),
        None
    )


    save_cart(cart)


    return redirect(
        url_for("cart.cart")
    )


# =========================================================
# CART COUNT
# =========================================================

@cart_bp.context_processor
def cart_count():

    cart = get_cart()


    count = 0


    for item in cart.values():

        try:

            count += int(
                item.get(
                    "quantity",
                    0
                )
            )

        except (TypeError, ValueError):

            pass


    return {
        "cart_count": count
    }