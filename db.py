import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r'congif\database.json')
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()
