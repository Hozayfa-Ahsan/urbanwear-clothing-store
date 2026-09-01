from flask import Flask, render_template

from config import Config
from models import db


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from models.product import Product

    from routes.products import products_bp
    from routes.cart import cart_bp
    from routes.chat import chat_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(chat_bp)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():

        products = Product.query.filter_by(
            is_featured=True
        ).limit(8).all()

        return render_template(
            "index.html",
            products=products
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
