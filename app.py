import os
import json
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify, render_template
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter

app = Flask(__name__)

# Initialize Firebase
# cred = credentials.Certificate('serviceAccountKey.json')

# Path to the service account key file
service_account_path = '/etc/secrets/serviceAccountKey.json'

cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crypto-chatbot-rasa-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Initialize Rasa agent
interpreter = RasaNLUInterpreter("models")
agent = Agent.load("models", interpreter=interpreter)

# Route to serve the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# Route for the webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    message = request.json.get('message')
    # Process the message with Rasa
    response_text = process_message(message)
    return jsonify({"message": response_text})

def process_message(message):
    # Fetch response from Rasa agent
    response = agent.handle_text(message)
    if response:
        response_text = response[0]['text']
    else:
        response_text = "I'm sorry, I don't understand that."
    return response_text

def get_crypto_data(crypto_name):
    try:
        ref = db.reference(f'cryptos/{crypto_name.lower()}')
        data = ref.get()
        if data:
            response = (
                f"{data['name']} ({data['symbol']}):\n"
                f"Current Price: ${data['current_price']}\n"
                f"Market Cap: ${data['market_cap']}\n"
                f"24h Volume: ${data['volume_24h']}\n"
                f"24h Price Change: {data['price_change_24h']:.2f}%\n"
                f"7d Price Change: {data['price_change_7d']:.2f}%"
            )
        else:
            response = f"No data found for {crypto_name}."
    except Exception as e:
        response = f"An error occurred: {str(e)}"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)