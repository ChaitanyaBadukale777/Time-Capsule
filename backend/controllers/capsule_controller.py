# backend/controllers/capsule_controller.py

from flask import Blueprint, request, jsonify
from datetime import date
from db_config import get_connection

capsule_bp = Blueprint("capsule_bp", __name__, url_prefix="/api/capsules")


@capsule_bp.route("", methods=["POST"])
def create_capsule():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()
    unlock_date = data.get("unlockDate", "").strip()

    errors = {}

    if not email:
        errors["email"] = "Email is required"
    if not unlock_date:
        errors["unlockDate"] = "Unlock date is required"
    if not message:
        errors["message"] = "Message is required"

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            INSERT INTO capsules (email, message, unlock_date, status)
            VALUES (%s, %s, %s, 'LOCKED')
            """,
            (email, message, unlock_date)
        )
        conn.commit()
        capsule_id = cursor.lastrowid

        cursor.execute(
            "SELECT * FROM capsules WHERE id = %s",
            (capsule_id,)
        )
        capsule = cursor.fetchone()
        return jsonify({"success": True, "capsule": capsule}), 201

    except Exception as e:
        print("Error creating capsule:", e)
        conn.rollback()
        return jsonify({"success": False, "error": "Internal Server Error"}), 500

    finally:
        cursor.close()
        conn.close()


@capsule_bp.route("", methods=["GET"])
def get_capsules():
    """
    Returns all capsules. Status is recalculated based on today's date.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM capsules ORDER BY created_at DESC")
        capsules = cursor.fetchall()

        today_str = str(date.today())

        # Auto-adjust status for frontend (does not update DB here)
        for c in capsules:
            if c["status"] == "LOCKED" and str(c["unlock_date"]) <= today_str:
                c["status"] = "UNLOCKED"

        return jsonify({"success": True, "capsules": capsules}), 200

    except Exception as e:
        print("Error fetching capsules:", e)
        return jsonify({"success": False, "error": "Internal Server Error"}), 500

    finally:
        cursor.close()
        conn.close()


@capsule_bp.route("/<int:capsule_id>", methods=["PUT"])
def update_capsule(capsule_id):
    """
    Update email, message, or unlock_date for a capsule.
    """
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()
    unlock_date = data.get("unlockDate", "").strip()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            UPDATE capsules
            SET email = %s, message = %s, unlock_date = %s
            WHERE id = %s
            """,
            (email, message, unlock_date, capsule_id)
        )
        conn.commit()

        cursor.execute("SELECT * FROM capsules WHERE id = %s", (capsule_id,))
        capsule = cursor.fetchone()

        if not capsule:
            return jsonify({"success": False, "error": "Capsule not found"}), 404

        return jsonify({"success": True, "capsule": capsule}), 200

    except Exception as e:
        print("Error updating capsule:", e)
        conn.rollback()
        return jsonify({"success": False, "error": "Internal Server Error"}), 500

    finally:
        cursor.close()
        conn.close()


@capsule_bp.route("/<int:capsule_id>", methods=["DELETE"])
def delete_capsule(capsule_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM capsules WHERE id = %s", (capsule_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Capsule not found"}), 404

        return jsonify({"success": True, "message": "Capsule deleted"}), 200

    except Exception as e:
        print("Error deleting capsule:", e)
        conn.rollback()
        return jsonify({"success": False, "error": "Internal Server Error"}), 500

    finally:
        cursor.close()
        conn.close()
