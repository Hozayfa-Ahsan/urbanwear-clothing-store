from datetime import datetime

from . import db


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    slug = db.Column(
        db.String(200),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    sale_price = db.Column(
        db.Float,
        nullable=True
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    style = db.Column(
        db.String(100),
        nullable=True
    )

    fabric = db.Column(
        db.String(100),
        nullable=True
    )

    color = db.Column(
        db.String(100),
        nullable=True
    )

    sizes = db.Column(
        db.String(200),
        nullable=True
    )

    stock = db.Column(
        db.Integer,
        default=0
    )

    image = db.Column(
        db.String(300),
        nullable=True
    )

    is_featured = db.Column(
        db.Boolean,
        default=False
    )

    is_new = db.Column(
        db.Boolean,
        default=False
    )

    is_sale = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def current_price(self):

        if self.sale_price is not None:
            return self.sale_price

        return self.price

    def available_sizes(self):

        if not self.sizes:
            return []

        return [
            size.strip()
            for size in self.sizes.split(",")
        ]