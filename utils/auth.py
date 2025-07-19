import firebase_admin.auth as auth
from flask import request, jsonify

def verify_firebase_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None, jsonify({"error": "Missing token"}), 401

    token = auth_header.split("Bearer ")[-1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token, None, None
    except Exception as e:
        return None, jsonify({"error": str(e)}), 401
