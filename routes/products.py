from flask import Blueprint, render_template, request

from models.product import Product


products_bp = Blueprint(
    "products",
    __name__
)


COLLECTIONS = {

    "men": {
        "name": "Men's Collection",
        "description": (
            "Refined essentials, modern tailoring and everyday "
            "pieces designed for the contemporary man."
        ),
        "image": (
            "https://images.unsplash.com/"
            "photo-1617137968427-85924c800a22"
            "?auto=format&fit=crop&w=2200&q=90"
        )
    },

    "women": {
        "name": "Women's Collection",
        "description": (
            "Elevated silhouettes, modern essentials and "
            "statement pieces designed to express your individuality."
        ),
        "image": (
            "https://images.unsplash.com/"
            "photo-1483985988355-763728e1935b"
            "?auto=format&fit=crop&w=2200&q=90"
        )
    },

    "kids": {
        "name": "Kids' Collection",
        "description": (
            "Comfortable, playful and stylish clothing "
            "made for every adventure."
        ),
        "image": (
            "https://images.unsplash.com/"
            "photo-1503919545889-aef636e10ad4"
            "?auto=format&fit=crop&w=2200&q=90"
        )
    },

    "unisex": {
        "name": "Unisex Apparel",
        "description": (
            "Effortless pieces without boundaries. "
            "Designed to be worn your way."
        ),
        "image": (
            "https://images.unsplash.com/"
            "photo-1529139574466-a303027c1d8b"
            "?auto=format&fit=crop&w=2200&q=90"
        )
    },

    "sale": {
        "name": "Sale & Clearance",
        "description": (
            "Exceptional styles at exceptional prices. "
            "Limited quantities available."
        ),
        "image": (
            "https://images.unsplash.com/"
            "photo-1445205170230-053b83016050"
            "?auto=format&fit=crop&w=2200&q=90"
        )
    }
}


def get_filter_values(products):

    sizes = set()
    colors = set()
    styles = set()
    fabrics = set()

    for product in products:

        if product.sizes:
            for size in product.sizes.split(","):
                size = size.strip()
                if size:
                    sizes.add(size)

        if product.color:
            colors.add(product.color.strip())

        if product.style:
            styles.add(product.style.strip())

        if product.fabric:
            fabrics.add(product.fabric.strip())

    return (
        sorted(sizes),
        sorted(colors),
        sorted(styles),
        sorted(fabrics)
    )


def product_matches_filters(
    product,
    selected_sizes,
    selected_colors,
    selected_styles,
    selected_fabrics,
    selected_price
):

    # SIZE
    if selected_sizes:

        product_sizes = []

        if product.sizes:
            product_sizes = [
                size.strip().lower()
                for size in product.sizes.split(",")
            ]

        if not any(
            size.lower() in product_sizes
            for size in selected_sizes
        ):
            return False

    # COLOR
    if selected_colors:

        if not product.color:
            return False

        if product.color.lower() not in [
            color.lower()
            for color in selected_colors
        ]:
            return False

    # STYLE
    if selected_styles:

        if not product.style:
            return False

        if product.style.lower() not in [
            style.lower()
            for style in selected_styles
        ]:
            return False

    # FABRIC
    if selected_fabrics:

        if not product.fabric:
            return False

        if product.fabric.lower() not in [
            fabric.lower()
            for fabric in selected_fabrics
        ]:
            return False

    # PRICE
    if selected_price:

        price = product.current_price()

        if selected_price == "0-50":

            if price >= 50:
                return False

        elif selected_price == "50-100":

            if price < 50 or price > 100:
                return False

        elif selected_price == "100-200":

            if price < 100 or price > 200:
                return False

        elif selected_price == "200+":

            if price < 200:
                return False

    return True


def apply_sorting(products, sort_by):

    if sort_by == "price-low":

        products.sort(
            key=lambda product: product.current_price()
        )

    elif sort_by == "price-high":

        products.sort(
            key=lambda product: product.current_price(),
            reverse=True
        )

    elif sort_by == "best-selling":

        products.sort(
            key=lambda product: product.stock,
            reverse=True
        )

    else:

        products.sort(
            key=lambda product: (
                product.created_at
                if product.created_at
                else 0
            ),
            reverse=True
        )

    return products


def collection_page(collection_key):

    collection = COLLECTIONS[collection_key]

    # -----------------------------------------------------
    # GET PRODUCTS
    # -----------------------------------------------------

    if collection_key == "sale":

        products = Product.query.filter_by(
            is_sale=True
        ).all()

    else:

        products = Product.query.filter_by(
            category=collection_key
        ).all()

    # -----------------------------------------------------
    # FILTER OPTIONS
    # -----------------------------------------------------

    sizes, colors, styles, fabrics = get_filter_values(
        products
    )

    # -----------------------------------------------------
    # REQUEST FILTERS
    # -----------------------------------------------------

    selected_sizes = request.args.getlist("size")

    selected_colors = request.args.getlist("color")

    selected_styles = request.args.getlist("style")

    selected_fabrics = request.args.getlist("fabric")

    selected_price = request.args.get(
        "price",
        ""
    )

    sort_by = request.args.get(
        "sort",
        "newest"
    )

    # -----------------------------------------------------
    # APPLY FILTERS
    # -----------------------------------------------------

    products = [
        product
        for product in products
        if product_matches_filters(
            product,
            selected_sizes,
            selected_colors,
            selected_styles,
            selected_fabrics,
            selected_price
        )
    ]

    # -----------------------------------------------------
    # SORT
    # -----------------------------------------------------

    products = apply_sorting(
        products,
        sort_by
    )

    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    return render_template(
        "collection.html",

        collection_name=collection["name"],

        collection_description=collection["description"],

        collection_image=collection["image"],

        collection_slug=collection_key,

        products=products,

        sizes=sizes,

        colors=colors,

        styles=styles,

        fabrics=fabrics,

        selected_sizes=selected_sizes,

        selected_colors=selected_colors,

        selected_styles=selected_styles,

        selected_fabrics=selected_fabrics,

        selected_price=selected_price,

        sort_by=sort_by
    )


# =========================================================
# COLLECTION ROUTES
# =========================================================

@products_bp.route("/men")
def men():

    return collection_page("men")


@products_bp.route("/women")
def women():

    return collection_page("women")


@products_bp.route("/kids")
def kids():

    return collection_page("kids")


@products_bp.route("/unisex")
def unisex():

    return collection_page("unisex")


@products_bp.route("/sale")
def sale():

    return collection_page("sale")


# =========================================================
# PRODUCT DETAIL
# =========================================================

@products_bp.route("/product/<slug>")
def product_detail(slug):

    product = Product.query.filter_by(
        slug=slug
    ).first_or_404()

    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(4).all()

    return render_template(
        "product_detail.html",
        product=product,
        related_products=related_products
    )