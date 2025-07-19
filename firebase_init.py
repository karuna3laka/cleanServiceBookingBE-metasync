import firebase_admin
from firebase_admin import credentials, firestore

# Use your service account key JSON
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
