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

@app.route('/')
def index():
    with open('index.html', 'r') as file:
        return render_template_string(file.read())

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    user_message = req.get("message")

    # Send message to Rasa
    response = requests.post(
        'http://localhost:5005/webhooks/rest/webhook',
        json={"sender": "user", "message": user_message}
    )

    response_text = ""
    if response.status_code == 200:
        response_json = response.json()
        if response_json:
            response_text = response_json[0].get("text", "")
        else:
            response_text = "Sorry, I didn't get that."
    else:
        response_text = "Error communicating with Rasa server."

    return jsonify({"message": response_text})

@app.route('/get_crypto_data/<crypto>', methods=['GET'])
def get_crypto_data(crypto):
    crypto_data_ref = db.reference(f'cryptos/{crypto}')
    crypto_data = crypto_data_ref.get()
    
    if crypto_data:
        return jsonify(crypto_data)
    else:
        return jsonify({"error": "No data found for the requested cryptocurrency."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
