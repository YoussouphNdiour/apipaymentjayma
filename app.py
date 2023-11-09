# Importations nécessaires
import os
import json 
from flask import Flask, request, jsonify, render_template
import requests

# Création de l'application Flask
app = Flask(__name__)

# Clés d'authentification
CLIENT_ID = "b3ad2ee4-883c-45eb-9844-5ebe656c8399"
CLIENT_SECRET = "cc441c0c-7af0-463e-bd55-1529cdab0e5d"

# URL du point de terminaison One Step Payment
PAYMENT_URL = "https://api.sandbox.orange-sonatel.com/api/eWallet/v1/payments/onestep"

# URL de l'API Checkout de Wave
WAVE_CHECKOUT_API_URL = "https://api.wave.com/v1/checkout/sessions"

# Obtenir un jeton d'accès
def get_access_token():
    auth_url = "https://api.sandbox.orange-sonatel.com/oauth/token"
    curl_command = f'curl -k -d client_id={CLIENT_ID} -d client_secret={CLIENT_SECRET} -d grant_type=client_credentials {auth_url}'
    response = os.popen(curl_command).read()
    try:
        access_token = json.loads(response).get("access_token")
        print(access_token)
        return access_token
    except Exception as e:
        print(f"Error getting access token: {str(e)}")
        return None

# Route pour créer une session de paiement avec Wave
@app.route("/create-wave-checkout-session", methods=["POST"])
def create_wave_checkout_session():
    # Obtenir les données du corps de la requête JSON
    data = requests.Response.json()

    # # Obtenir un jeton d'accès
    # access_token = get_access_token()
    # if not access_token:
    #     return jsonify({"error": "Failed to obtain access token"}), 500

    # Inclure le jeton d'accès dans les en-têtes de la requête
    headers = {
        # "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Effectuer la requête pour créer une session de paiement avec Wave
    response = requests.post(WAVE_CHECKOUT_API_URL, json=data, headers=headers)
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify(response.json()), response.status_code

# Route pour récupérer les détails d'une session de paiement avec Wave
@app.route("/get-wave-checkout-session/<session_id>", methods=["GET"])
def get_wave_checkout_session(session_id):
    # Obtenir un jeton d'accès
    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to obtain access token"}), 500

    # Inclure le jeton d'accès dans les en-têtes de la requête
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Construire l'URL de l'API Checkout de Wave avec l'identifiant de session
    wave_checkout_session_url = f"{WAVE_CHECKOUT_API_URL}/{session_id}"

    # Effectuer la requête pour obtenir les détails de la session de paiement avec Wave
    response = requests.get(wave_checkout_session_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return jsonify(response.json()), response.status_code
@app.route("/")
def hello_world():
    return "render_template('home.html')"

@app.route('/onestep-payment', methods=['POST'])
def one_step_payment():
    # Obtenir les données du corps de la requête JSON
    data = request.json
    print(request)

    # Obtenir un jeton d'accès
    access_token = get_access_token()
    print(access_token)
    if not access_token:
        return jsonify({"error": "Failed to obtain access token"}), 500

    # Inclure le jeton d'accès dans les en-têtes de la requête
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Effectuer la requête One Step Payment
    response = requests.post(PAYMENT_URL, json=data, headers=headers)
    print(access_token)
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify(response.json()), response.status_code
    
# Point d'entrée principal pour exécuter l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
