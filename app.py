import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize Firebase
# cred = credentials.Certificate('serviceAccountKey.json')

# Path to the service account key file
service_account_path = '/etc/secrets/serviceAccountKey.json'

cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crypto-chatbot-rasa-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

@app.route('/webhook', methods=['POST'])
def webhook():
    message = request.json.get('message')
    # Your Rasa interaction logic
    response = {"message": "This is a placeholder response"}
    return jsonify(response)

@app.route('/')
def index():
    return "Hello! This is the Crypto Chatbot server."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
