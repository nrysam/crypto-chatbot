import firebase_admin
from firebase_admin import credentials, db
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crypto-chatbot-rasa-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

class ActionGetCryptoData(Action):
    def name(self) -> Text:
        return "action_get_crypto_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        crypto = tracker.get_slot('crypto').lower()
        crypto_data_ref = db.reference(f'cryptos/{crypto}')
        crypto_data = crypto_data_ref.get()
        
        if crypto_data:
            response = (
                f"Here's the data for {crypto.capitalize()}:\n"
                f"Current Price: ${crypto_data['current_price']}\n"
                f"Market Cap: ${crypto_data['market_cap']}\n"
                f"24h Volume: ${crypto_data['volume_24h']}\n"
                f"Price Change (24h): {crypto_data['price_change_24h']:.2f}%\n"
                f"Price Change (7d): {crypto_data['price_change_7d']:.2f}%\n"
            )
        else:
            response = f"Sorry, I don't have data for {crypto.capitalize()}."

        dispatcher.utter_message(text=response)
        return []