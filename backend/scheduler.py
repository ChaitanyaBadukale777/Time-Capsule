# backend/scheduler.py

import time
from datetime import date
import schedule
from db_config import get_connection
from email_service import send_unlock_email


def check_and_unlock_capsules():
    today_str = str(date.today())
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get all capsules that should unlock today or earlier and are still LOCKED
        cursor.execute(
            """
            SELECT id, email, message, unlock_date
            FROM capsules
            WHERE status = 'LOCKED' AND unlock_date <= %s
            """,
            (today_str,)
        )
        rows = cursor.fetchall()

        for row in rows:
            capsule_id = row["id"]
            email = row["email"]
            msg = row["message"]
            unlock_date = str(row["unlock_date"])

            # Send email
            send_unlock_email(email, msg, unlock_date)

            # Update status to UNLOCKED in DB
            cursor.execute(
                "UPDATE capsules SET status = 'UNLOCKED' WHERE id = %s",
                (capsule_id,)
            )

        conn.commit()

        if rows:
            print(f"Unlocked & notified {len(rows)} capsule(s).")

    except Exception as e:
        print("Error in scheduler:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def main():
    # Run once at startup
    check_and_unlock_capsules()

    # Schedule daily at 09:00
    schedule.every().day.at("09:00").do(check_and_unlock_capsules)

    print("Scheduler started. Waiting for unlock time...")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
