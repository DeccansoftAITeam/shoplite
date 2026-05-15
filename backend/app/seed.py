from decimal import Decimal

from sqlalchemy import func, select

from app.core.db import Base, SessionLocal, engine
from app.modules.catalog.models import Product

SAMPLE_PRODUCTS = [
    {
        "name": "Classic White T-Shirt",
        "description": "Soft cotton crew neck t-shirt",
        "price": Decimal("12.99"),
        "stock": 120,
    },
    {
        "name": "Slim Fit Jeans",
        "description": "Dark blue denim with stretch",
        "price": Decimal("39.50"),
        "stock": 60,
    },
    {
        "name": "Canvas Trainers",
        "description": "Lightweight everyday trainers",
        "price": Decimal("29.99"),
        "stock": 45,
    },
    {
        "name": "Zip Hoodie",
        "description": "Fleece-lined hoodie in charcoal",
        "price": Decimal("34.00"),
        "stock": 35,
    },
    {
        "name": "Wool Beanie",
        "description": "Rib-knit beanie for cold weather",
        "price": Decimal("11.25"),
        "stock": 80,
    },
    {
        "name": "Leather Wallet",
        "description": "Bi-fold wallet with card slots",
        "price": Decimal("24.75"),
        "stock": 50,
    },
    {
        "name": "Sports Socks (3 Pack)",
        "description": "Breathable cushioned socks",
        "price": Decimal("9.99"),
        "stock": 200,
    },
    {
        "name": "Utility Backpack",
        "description": "Water-resistant daily backpack",
        "price": Decimal("44.90"),
        "stock": 40,
    },
    {
        "name": "Polarised Sunglasses",
        "description": "UV-protection sunglasses",
        "price": Decimal("19.80"),
        "stock": 70,
    },
    {
        "name": "Running Shorts",
        "description": "Quick-dry lightweight shorts",
        "price": Decimal("17.60"),
        "stock": 90,
    },
]


def seed_products() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        existing_count = db.scalar(select(func.count(Product.id)))
        if existing_count and existing_count > 0:
            print("Seed skipped: products already exist.")
            return

        db.add_all(
            [
                Product(
                    name=item["name"],
                    description=item["description"],
                    price=item["price"],
                    stock=item["stock"],
                )
                for item in SAMPLE_PRODUCTS
            ]
        )
        db.commit()

    print("Seed complete: inserted 10 sample products.")


if __name__ == "__main__":
    seed_products()
