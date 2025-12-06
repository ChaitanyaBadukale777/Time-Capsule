
# import random
# from flask import Blueprint, request, jsonify
# from db_config import get_connection
# from sms_service import send_otp_sms

# otp_bp = Blueprint("otp_bp", __name__, url_prefix="/api/otp")


# @otp_bp.route("/start", methods=["POST"])
# def start_otp():
#     """
#     Step 1: User fills email, phone, message, unlockDate.
#     We generate an OTP, store all data in pending_capsules,
#     send SMS, and return the pendingId.
#     """
#     data = request.get_json() or {}

#     email = (data.get("email") or "").strip()
#     phone = (data.get("phone") or "").strip()
#     message = (data.get("message") or "").strip()
#     unlock_date = (data.get("unlockDate") or "").strip()

#     errors = {}
#     if not email:
#         errors["email"] = "Email is required"
#     if not phone:
#         errors["phone"] = "Phone is required"
#     if not message:
#         errors["message"] = "Message is required"
#     if not unlock_date:
#         errors["unlockDate"] = "Unlock date is required"

#     if errors:
#         return jsonify({"success": False, "errors": errors}), 400

#     otp = str(random.randint(100000, 999999))

#     conn = get_connection()
#     cursor = conn.cursor()

#     try:
#         cursor.execute(
#             """
#             INSERT INTO pending_capsules (email, phone, message, unlock_date, otp)
#             VALUES (%s, %s, %s, %s, %s)
#             """,
#             (email, phone, message, unlock_date, otp)
#         )
#         conn.commit()
#         pending_id = cursor.lastrowid

#         sms_ok = send_otp_sms(phone, otp)
#         if not sms_ok:
#             print("[WARN] SMS sending failed for phone:", phone)

#         return jsonify({
#             "success": True,
#             "pendingId": pending_id,
#             "message": "OTP sent successfully"
#         }), 200

#     except Exception as e:
#         print("[OTP START ERROR]", e)
#         conn.rollback()
#         return jsonify({"success": False, "error": "Internal Server Error"}), 500

#     finally:
#         cursor.close()
#         conn.close()


# @otp_bp.route("/verify", methods=["POST"])
# def verify_otp():
#     """
#     Step 2: User sends pendingId + otp.
#     If valid, we move data from pending_capsules → capsules table.
#     """
#     data = request.get_json() or {}

#     pending_id = data.get("pendingId")
#     otp = (data.get("otp") or "").strip()

#     if not pending_id or not otp:
#         return jsonify({"success": False, "message": "pendingId and otp are required"}), 400

#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)

#     try:
#         cursor.execute(
#             "SELECT * FROM pending_capsules WHERE id = %s",
#             (pending_id,)
#         )
#         pending = cursor.fetchone()

#         if not pending:
#             return jsonify({"success": False, "message": "Session expired or invalid"}), 404

#         if pending["otp"] != otp:
#             return jsonify({"success": False, "message": "Invalid OTP"}), 400

#         email = pending["email"]
#         phone = pending["phone"]
#         message = pending["message"]
#         unlock_date = pending["unlock_date"]

#         cursor2 = conn.cursor()
#         cursor2.execute(
#             """
#             INSERT INTO capsules (email, message, unlock_date, status)
#             VALUES (%s, %s, %s, 'LOCKED')
#             """,
#             (email, message, unlock_date)
#         )

#         cursor.execute(
#             "DELETE FROM pending_capsules WHERE id = %s",
#             (pending_id,)
#         )

#         conn.commit()
#         cursor2.close()

#         return jsonify({"success": True, "message": "OTP verified & capsule saved"}), 200

#     except Exception as e:
#         print("[OTP VERIFY ERROR]", e)
#         conn.rollback()
#         return jsonify({"success": False, "message": "Internal Server Error"}), 500

#     finally:
#         cursor.close()
#         conn.close()
