from pathlib import Path
from urllib.request import urlopen, Request

from app import app
from models import db
from models.product import Product


PRODUCT_IMAGE_DIR = Path(
    "static/images/products"
)


PRODUCT_IMAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


products = [

    # =====================================================
    # MEN
    # =====================================================

    {
        "name": "Essential Black Tee",
        "slug": "essential-black-tee",
        "description": (
            "A clean everyday essential crafted "
            "for effortless streetwear styling. "
            "Soft cotton fabric with a relaxed modern fit."
        ),
        "price": 29.00,
        "sale_price": None,
        "category": "men",
        "style": "Casual",
        "fabric": "100% Cotton",
        "color": "Black",
        "sizes": "S,M,L,XL,XXL",
        "stock": 35,
        "image": "images/products/essential-black-tee.jpg",
        "is_featured": True,
        "is_new": True,
        "is_sale": False,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1521572163474-6864f9cf17ab"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },

    {
        "name": "Urban Denim Jacket",
        "slug": "urban-denim-jacket",
        "description": (
            "A timeless denim jacket designed "
            "for everyday layering. Structured "
            "silhouette with a versatile urban finish."
        ),
        "price": 69.00,
        "sale_price": 54.00,
        "category": "men",
        "style": "Streetwear",
        "fabric": "Denim",
        "color": "Blue",
        "sizes": "S,M,L,XL",
        "stock": 18,
        "image": "images/products/urban-denim-jacket.jpg",
        "is_featured": True,
        "is_new": False,
        "is_sale": True,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1495105787522-5334e3ffa0ef"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },

    {
        "name": "Premium Oversized Hoodie",
        "slug": "premium-oversized-hoodie",
        "description": (
            "Heavyweight fleece hoodie with an "
            "oversized silhouette, soft interior "
            "and premium everyday comfort."
        ),
        "price": 59.00,
        "sale_price": None,
        "category": "men",
        "style": "Streetwear",
        "fabric": "Cotton Fleece",
        "color": "Charcoal",
        "sizes": "S,M,L,XL,XXL",
        "stock": 25,
        "image": "images/products/premium-oversized-hoodie.jpg",
        "is_featured": True,
        "is_new": True,
        "is_sale": False,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1556821840-3a63f95609a7"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },


    # =====================================================
    # WOMEN
    # =====================================================

    {
        "name": "Midnight Satin Dress",
        "slug": "midnight-satin-dress",
        "description": (
            "An elegant satin-inspired silhouette "
            "designed for evenings, celebrations "
            "and elevated occasions."
        ),
        "price": 79.00,
        "sale_price": 64.00,
        "category": "women",
        "style": "Evening",
        "fabric": "Satin",
        "color": "Black",
        "sizes": "XS,S,M,L,XL",
        "stock": 14,
        "image": "images/products/midnight-satin-dress.jpg",
        "is_featured": True,
        "is_new": False,
        "is_sale": True,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1496747611176-843222e1e57c"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },

    {
        "name": "Modern Beige Blazer",
        "slug": "modern-beige-blazer",
        "description": (
            "A refined blazer with a clean tailored "
            "shape that transitions effortlessly "
            "from office hours to evening styling."
        ),
        "price": 89.00,
        "sale_price": None,
        "category": "women",
        "style": "Tailored",
        "fabric": "Polyester Blend",
        "color": "Beige",
        "sizes": "XS,S,M,L,XL",
        "stock": 16,
        "image": "images/products/modern-beige-blazer.jpg",
        "is_featured": True,
        "is_new": True,
        "is_sale": False,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1551488831-00ddcb6c6bd3"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },

    {
        "name": "Relaxed Everyday Top",
        "slug": "relaxed-everyday-top",
        "description": (
            "A versatile everyday top with a relaxed "
            "fit and lightweight construction for "
            "comfortable all-day wear."
        ),
        "price": 39.00,
        "sale_price": 31.00,
        "category": "women",
        "style": "Casual",
        "fabric": "Cotton Blend",
        "color": "White",
        "sizes": "XS,S,M,L",
        "stock": 22,
        "image": "images/products/relaxed-everyday-top.jpg",
        "is_featured": False,
        "is_new": False,
        "is_sale": True,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1485968579580-b6d095142e6e"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },


    # =====================================================
    # KIDS
    # =====================================================

    {
        "name": "Mini Explorer Set",
        "slug": "mini-explorer-set",
        "description": (
            "A comfortable kids' outfit designed "
            "for everyday adventures, playtime "
            "and relaxed weekend styling."
        ),
        "price": 35.00,
        "sale_price": None,
        "category": "kids",
        "style": "Casual",
        "fabric": "Cotton",
        "color": "Olive",
        "sizes": "2Y,4Y,6Y,8Y,10Y",
        "stock": 20,
        "image": "images/products/mini-explorer-set.jpg",
        "is_featured": True,
        "is_new": True,
        "is_sale": False,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1503919545889-aef636e10ad4"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },

    {
        "name": "Little Star Dress",
        "slug": "little-star-dress",
        "description": (
            "A playful and comfortable children's "
            "dress made for parties, family outings "
            "and special moments."
        ),
        "price": 42.00,
        "sale_price": 34.00,
        "category": "kids",
        "style": "Party",
        "fabric": "Cotton Blend",
        "color": "Pink",
        "sizes": "2Y,4Y,6Y,8Y",
        "stock": 12,
        "image": "images/products/little-star-dress.jpg",
        "is_featured": False,
        "is_new": False,
        "is_sale": True,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1518831959646-742c3a14ebf7"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },


    # =====================================================
    # UNISEX
    # =====================================================

    {
        "name": "Essential Oversized Hoodie",
        "slug": "essential-unisex-hoodie",
        "description": (
            "A gender-neutral oversized hoodie "
            "with a minimal aesthetic, heavyweight "
            "feel and everyday streetwear appeal."
        ),
        "price": 62.00,
        "sale_price": 49.00,
        "category": "unisex",
        "style": "Streetwear",
        "fabric": "Cotton Fleece",
        "color": "Black",
        "sizes": "XS,S,M,L,XL,XXL",
        "stock": 30,
        "image": "images/products/essential-unisex-hoodie.jpg",
        "is_featured": True,
        "is_new": False,
        "is_sale": True,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1578681994506-b8f463449011"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },

    {
        "name": "Classic Neutral Sweatshirt",
        "slug": "classic-neutral-sweatshirt",
        "description": (
            "A clean neutral sweatshirt designed "
            "to pair easily with denim, trousers "
            "or relaxed weekend outfits."
        ),
        "price": 49.00,
        "sale_price": None,
        "category": "unisex",
        "style": "Minimal",
        "fabric": "Cotton Fleece",
        "color": "Cream",
        "sizes": "S,M,L,XL",
        "stock": 27,
        "image": "images/products/classic-neutral-sweatshirt.jpg",
        "is_featured": True,
        "is_new": True,
        "is_sale": False,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1485230895905-ec40ba36b9bc"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },


    # =====================================================
    # SALE
    # =====================================================

    {
        "name": "Weekend Cargo Pants",
        "slug": "weekend-cargo-pants",
        "description": (
            "Relaxed cargo pants with practical "
            "pockets and a contemporary silhouette "
            "for casual everyday outfits."
        ),
        "price": 65.00,
        "sale_price": 45.00,
        "category": "unisex",
        "style": "Utility",
        "fabric": "Cotton Twill",
        "color": "Khaki",
        "sizes": "S,M,L,XL",
        "stock": 19,
        "image": "images/products/weekend-cargo-pants.jpg",
        "is_featured": True,
        "is_new": False,
        "is_sale": True,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1515886657613-9f3515b0c78f"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },

    {
        "name": "Classic Denim Jeans",
        "slug": "classic-denim-jeans",
        "description": (
            "A timeless denim essential with a "
            "comfortable modern fit, designed to "
            "work with almost any wardrobe."
        ),
        "price": 59.00,
        "sale_price": 44.00,
        "category": "men",
        "style": "Casual",
        "fabric": "Denim",
        "color": "Indigo",
        "sizes": "30,32,34,36,38",
        "stock": 24,
        "image": "images/products/classic-denim-jeans.jpg",
        "is_featured": True,
        "is_new": False,
        "is_sale": True,
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1542272604-787c3835535d"
            "?auto=format&fit=crop&w=1000&q=85"
        ),
    },

]


def download_image(url, destination):

    if destination.exists():

        print(
            f"Image already exists: "
            f"{destination.name}"
        )

        return


    print(
        f"Downloading: {destination.name}"
    )


    request = Request(
        url,
        headers={
            "User-Agent": "UrbanWear/1.0"
        }
    )


    with urlopen(
        request,
        timeout=30
    ) as response:

        data = response.read()


    destination.write_bytes(data)


def seed_products():

    with app.app_context():

        db.create_all()


        added = 0

        skipped = 0


        for data in products:

            existing = Product.query.filter_by(
                slug=data["slug"]
            ).first()


            if existing:

                print(
                    f"Already exists: "
                    f"{data['name']}"
                )

                skipped += 1

                continue


            image_path = Path(
                "static"
            ) / data["image"]


            download_image(
                data["image_url"],
                image_path
            )


            product = Product(

                name=data["name"],

                slug=data["slug"],

                description=data["description"],

                price=data["price"],

                sale_price=data["sale_price"],

                category=data["category"],

                style=data["style"],

                fabric=data["fabric"],

                color=data["color"],

                sizes=data["sizes"],

                stock=data["stock"],

                image=data["image"],

                is_featured=data["is_featured"],

                is_new=data["is_new"],

                is_sale=data["is_sale"],

            )


            db.session.add(product)

            added += 1


        db.session.commit()


        print()
        print("=" * 50)
        print("URBANWEAR PRODUCT SEED COMPLETE")
        print("=" * 50)
        print(f"Products added : {added}")
        print(f"Products skipped: {skipped}")
        print("=" * 50)


if __name__ == "__main__":

    seed_products()