from fetch_payments import fetch_all_payments
from helpers import log, setup_logging
from database import init_db, upsert_payments, count_payments


def main():
    setup_logging()
    init_db()

    payments = fetch_all_payments()
    inserted, updated = upsert_payments(payments)

    log.info(f"Inserted {inserted}, updated {updated}, total in DB: {count_payments()}")


if __name__ == "__main__":
    main()

