from datetime import date
import time
import schedule

from db_config import get_connection
from email_service import send_unlock_email


def check_and_unlock_capsules():
    today_str = str(date.today())
    print(f"[SCHEDULER] Checking capsules for date <= {today_str}")

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

        if not rows:
            print("[SCHEDULER] No capsules to unlock.")
        else:
            print(f"[SCHEDULER] Found {len(rows)} capsule(s) to unlock.")

        for row in rows:
            capsule_id = row["id"]
            email = row["email"]
            msg = row["message"]
            unlock_date_str = str(row["unlock_date"])

            # Send email
            ok = send_unlock_email(email, msg, unlock_date_str)

            # If email sent, update DB status
            if ok:
                cursor.execute(
                    "UPDATE capsules SET status = 'UNLOCKED' WHERE id = %s",
                    (capsule_id,)
                )
                print(f"[SCHEDULER] Capsule {capsule_id} marked as UNLOCKED.")

        conn.commit()

    except Exception as e:
        print("[SCHEDULER ERROR]", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def main():
    # Run once at startup
    check_and_unlock_capsules()

    # Then schedule it daily at 09:00 AM
    schedule.every().day.at("09:00").do(check_and_unlock_capsules)

    print("[SCHEDULER] Started. Waiting for next run...")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
