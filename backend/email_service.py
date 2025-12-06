# backend/email_service.py

import smtplib
from email.message import EmailMessage

# 🔧 CHANGE THESE
SENDER_EMAIL = "dexyyy777@gmail.com"
APP_PASSWORD = "zfshsxxbqzmomrod"  # from Google App Passwords


def send_unlock_email(to_email: str, message_text: str, unlock_date: str):
    """
    Sends an email when a capsule is unlocked.
    """
    msg = EmailMessage()
    msg["Subject"] = "Your Digital Time Capsule is Unlocked ✨"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    html_body = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 25px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
      
      <h2 style="color: #0ea5e9; text-align: center;">
        🎉 Your Digital Time Capsule Has Been Unlocked 🎉
      </h2>

      <p><b>Scheduled Unlock Date:</b> {unlock_date}</p>

      <hr>

      <h3 style="color: #111827;">📝 Your Message to the Future You:</h3>
      <div style="background: #f1f5f9; padding: 15px; border-radius: 6px; font-size: 15px; line-height: 1.6;">
        <b>{message_text}</b>
      </div>

      <p style="margin-top: 20px; font-style: italic; color: #374151;">
        कभी जो लिखा था उम्मीदों के नाम,<br>
        आज वही पैग़ाम बनकर लौटा है तुम्हारे नाम।
      </p>

      <p style="color: #374151;">
        Take a moment to reflect on how far you’ve come and where you’re headed next.
      </p>

      <hr>

      <p style="font-size: 13px; color: #6b7280;">
        If you did not create this capsule, please ignore this email.
      </p>

      <p style="margin-top: 20px;">
        Warm Regards,<br>
        <b>Digital Time Capsule Team</b>
      </p>
    </div>
  </body>
</html>
"""

    msg.set_content("Your mail client does not support HTML.")
    msg.add_alternative(html_body, subtype="html")


    try:
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login(SENDER_EMAIL, APP_PASSWORD)
      server.send_message(msg)
      server.quit()
      print(f"Email sent to {to_email}")
    except Exception as e:
      print("Error sending email:", e)
