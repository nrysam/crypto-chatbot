from flask import Flask, jsonify
import json

app = Flask(__name__)

def load_crypto_data():
    with open('crypto_data.json', 'r') as f:
        return json.load(f)

@app.route('/crypto/<crypto_id>', methods=['GET'])
def get_crypto_data(crypto_id):
    crypto_data = load_crypto_data()
    data = crypto_data.get(crypto_id)
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Cryptocurrency not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)