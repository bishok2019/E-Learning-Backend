from decimal import Decimal

from sqlalchemy.orm import Session

from apps.course.models import Currency
from apps.database import SessionLocal

CURRENCIES = [
    {
        "code": "NPR",
        "name": "Nepalese Rupee",
        "symbol": "रू",
        "decimal_places": 2,
    },
    {
        "code": "USD",
        "name": "United States Dollar",
        "symbol": "$",
        "decimal_places": 2,
    },
    {
        "code": "INR",
        "name": "Indian Rupee",
        "symbol": "₹",
        "decimal_places": 2,
    },
    {
        "code": "EUR",
        "name": "Euro",
        "symbol": "€",
        "decimal_places": 2,
    },
    {
        "code": "GBP",
        "name": "British Pound",
        "symbol": "£",
        "decimal_places": 2,
    },
]


def seed_currencies():
    db: Session = SessionLocal()

    try:
        for currency_data in CURRENCIES:
            currency = (
                db.query(Currency)
                .filter(Currency.code == currency_data["code"])
                .first()
            )

            if currency:
                print(f"Currency {currency_data['code']} already exists. Skipping.")
                continue

            currency = Currency(
                **currency_data,
                is_active=True,
                is_deleted=False,
            )

            db.add(currency)

        db.commit()

        print("Currencies seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_currencies()
