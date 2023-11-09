import os
import json 
from flask import Flask, request, jsonify, render_template
from urllib import request
app = Flask(__name__)

# Clés d'authentification
CLIENT_ID = "b3ad2ee4-883c-45eb-9844-5ebe656c8399"
CLIENT_SECRET = "cc441c0c-7af0-463e-bd55-1529cdab0e5d"

# URL du point de terminaison One Step Payment
PAYMENT_URL = "https://api.sandbox.orange-sonatel.com/api/eWallet/v1/payments/onestep"

# Obtenir un jeton d'accès
def get_access_token():
    auth_url = "https://api.sandbox.orange-sonatel.com/oauth/token"

    # Utilisez curl pour obtenir le jeton
    curl_command = f'curl -k -d client_id={CLIENT_ID} -d client_secret={CLIENT_SECRET} -d grant_type=client_credentials {auth_url}'
    response = os.popen(curl_command).read()
    try:
        access_token = json.loads(response).get("access_token")
        return access_token
    except Exception as e:
        print(f"Error getting access token: {str(e)}")
        return None
    
@app.route("/")
def hello_world():
    return "render_template('home.html')"

@app.route('/onestep-payment', methods=['POST'])
def one_step_payment():
    # Obtenir les données du corps de la requête JSON
    data = request.json

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
    print(response.status_code)
    # print(response.content)
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({"err":"eer"}), response.status_code
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)