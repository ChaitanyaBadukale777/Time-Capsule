
# import requests

# FAST2SMS_API_KEY = "YOUR_FAST2SMS_API_KEY_HERE"


# def send_otp_sms(phone: str, otp: str) -> bool:
#     """
#     Sends OTP via Fast2SMS to the given phone number.
#     Returns True if request did not error out.
#     """

#     url = "https://www.fast2sms.com/dev/bulkV2"

#     payload = {
#         "route": "otp",
#         "numbers": phone,
#         "variables_values": otp,
#     }

#     headers = {
#         "authorization": FAST2SMS_API_KEY,
#         "Content-Type": "application/json"
#     }

#     try:
#         response = requests.post(url, json=payload, headers=headers, timeout=10)
#         print("[SMS RESPONSE]", response.text)
#         return response.status_code == 200
#     except Exception as e:
#         print("[SMS ERROR]", e)
#         return False
