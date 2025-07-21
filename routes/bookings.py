from flask import Blueprint, request, jsonify
from firebase_init import db
from utils.auth import verify_firebase_token
import uuid

booking_bp = Blueprint("bookings", __name__)

#######################################

@booking_bp.route("/admin/bookings", methods=["GET"])
def get_all_bookings():
    user, error_response, status_code = verify_firebase_token()
    if error_response:
        return error_response, status_code

    # Only allow admins — you can add custom admin check logic here
    if user.get("email") not in ["admin@example.com"]:  # 🔒 update this
        return jsonify({"error": "Unauthorized"}), 403

    bookings_ref = db.collection("bookings")
    bookings = [doc.to_dict() | {"id": doc.id} for doc in bookings_ref.stream()]
    return jsonify(bookings), 200

################################################

# Create a new booking
@booking_bp.route("/bookings", methods=["POST"])
def create_booking():
    user, error_response, status_code = verify_firebase_token()
    if error_response:
        return error_response, status_code

    data = request.get_json()
    booking_id = str(uuid.uuid4())

    # Attach user data to booking
    data["user_id"] = user["uid"]
    data["user_email"] = user.get("email", "")
    data.setdefault("status", "Pending")  # Default booking status

    db.collection("bookings").document(booking_id).set(data)
    return jsonify({"message": "Booking created", "id": booking_id}), 201

# Retrieve bookings for the logged-in user
@booking_bp.route("/bookings", methods=["GET"])
def get_user_bookings():
    user, error_response, status_code = verify_firebase_token()
    if error_response:
        return error_response, status_code

    user_id = user["uid"]
    bookings_ref = db.collection("bookings").where("user_id", "==", user_id)
    bookings = [doc.to_dict() | {"id": doc.id} for doc in bookings_ref.stream()]
    return jsonify(bookings), 200

# Update a specific booking
@booking_bp.route("/bookings/<booking_id>", methods=["PUT"])
def update_booking(booking_id):
    user, error_response, status_code = verify_firebase_token()
    if error_response:
        return error_response, status_code

    data = request.get_json()
    db.collection("bookings").document(booking_id).update(data)
    return jsonify({"message": "Booking updated"}), 200

# Delete a specific booking
@booking_bp.route("/bookings/<booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    user, error_response, status_code = verify_firebase_token()
    if error_response:
        return error_response, status_code

    db.collection("bookings").document(booking_id).delete()
    return jsonify({"message": "Booking deleted"}), 200
