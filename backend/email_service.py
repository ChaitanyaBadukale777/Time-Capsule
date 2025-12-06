# backend/email_service.py

import smtplib
from email.message import EmailMessage

# 🔧 CHANGE THESE
SENDER_EMAIL = "yourgmail@gmail.com"
APP_PASSWORD = "YOUR_16_CHAR_APP_PASSWORD"  # from Google App Passwords


def send_unlock_email(to_email: str, message_text: str, unlock_date: str):
    """
    Sends an email when a capsule is unlocked.
    """
    msg = EmailMessage()
    msg["Subject"] = "Your Digital Time Capsule is Unlocked ✨"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    body = f"""
Your Digital Time Capsule set for {unlock_date} is now unlocked! 🎉

Here is your message:

{message_text}

— Digital Time Capsule
"""
    msg.set_content(body)

    try:
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login(SENDER_EMAIL, APP_PASSWORD)
      server.send_message(msg)
      server.quit()
      print(f"Email sent to {to_email}")
    except Exception as e:
      print("Error sending email:", e)
