# Crypto Chatbot

This is a Crypto Chatbot built using Rasa and Flask. It can answer questions about cryptocurrencies by fetching data from a Firebase database.

## Features

- Interactive chatbot for cryptocurrency information
- Fetches real-time data from Firebase
- Deployed using Flask
- Frontend with chat interface

## Requirements

- Python (3.8 to 3.10)
- Flask
- Firebase Admin SDK
- Rasa
- Pandas
- Scikit-learn

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/crypto-chatbot.git
    cd crypto-chatbot
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up Firebase:
    - Place your Firebase `serviceAccountKey.json` file in the `server` directory.

5. Train the Rasa model:
    ```bash
    rasa train
    ```

6. Run the Rasa server and action server:
    ```bash
    rasa run actions &
    rasa run
    ```

7. Run the Flask application:
    ```bash
    python app.py
    ```

8. Open your browser and go to `http://127.0.0.1:8000` to interact with the chatbot.

## Deployment

### Deploy on Render

1. Create an account on [Render](https://render.com/).

2. Create a new Web Service on Render and connect your GitHub repository.

3. Set the Build Command to:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    rasa train
    ```

4. Set the Start Command to:
    ```bash
    source /venv/bin/activate
    rasa run actions & rasa run -m models --enable-api --cors "*" --debug &
    python app.py
    ```

5. Add the service account key as a secret file:
    - Name the file `serviceAccountKey.json`.
    - Paste the entire content of your `serviceAccountKey.json` into the file.

6. Add Python version in environtment variable :
    - Key : PYTHON_VERSION 
    - Value : 3.10.0

7. Deploy the service and access it via the provided URL.

## License

This project is licensed under the MIT License.
