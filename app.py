from flask import Flask, render_template, request, make_response, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS
from email.message import EmailMessage
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_secure_default_key')

CORS(app, supports_credentials=True, allow_headers="*", origins="*", methods=["OPTIONS", "POST"])
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


client = MongoClient(
    'mongodb+srv://crob0008:GYfLnhxdJgeiOTPO@chefsbhojan.oxsu9gm.mongodb.net/',
    connectTimeoutMS=30000, 
    socketTimeoutMS=None)
dbC = client['FORMDATACOLLECTION']
Details = dbC['CONTACTS']
db = client['ORDERS']
CB_PONDA = db['CB_PONDA']
CB_MARGAO = db['CB_MARGAO']

@app.route('/api/save_form_data', methods=['POST', 'OPTIONS'])
def save_form_data():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success', 'message': 'CORS preflight request handled successfully'}), 200
    
    data = request.json
    print("Received form data:", data)
    
    new_contact = {
        'name' :data['name'],
        'phone':data['phone'],
        'date_created': datetime.utcnow()
    }
    Details.insert_one(new_contact)
    print(data)
    return jsonify({'status': 'success', 'message': 'Form data saved successfully'}), 200

ALLOWED_PINCODES_PONDA = [
    "403401",  # Ponda
    "403102",  # Agapur Adpoi
    "403401",  # Bandora
    "403103",  # Shiroda
    "403404",  # Mardol
    "403706",  # Usgao
    "403406"   # Borim
]

ALLOWED_PINCODES_MARGAO = [
    "403707",  # Margao
    "403708",  # Aquem
    "403709",  # Navelim
    "403710",  # Fatorda
    "403711",  # Borda
    "403712",  # Colva
    "403713"   # Benaulim
]

@app.route('/api/orders', methods=['POST', 'OPTIONS'])
def save_form_data():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success', 'message': 'CORS preflight request handled successfully'}), 200
    
    data = request.json
    print("Received form data:", data)
    
    pincode = data.get('pincode')
    outlet_selected = data.get('selectedOutlet')

    if outlet_selected == 'Ponda':
        if pincode in ALLOWED_PINCODES_PONDA:
            new_order = {
                'orderId': data['orderId'],
                'name' : data['name'],
                'phone': data['phone'],
                'address': data['address'],
                'pincode': data['pincode'],
                'items' : data['items'],
                'date_created': data['date'],
                'fulfilled': False
            }
            CB_PONDA.insert_one(new_order)
            return jsonify({'status': 'success', 'message': 'Form data saved successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Delivery not available for the entered pincode'}), 400
    
    elif outlet_selected == 'Margao':
        if pincode in ALLOWED_PINCODES_MARGAO:
            new_order = {
                'orderId': data['orderId'],
                'name' : data['name'],
                'phone': data['phone'],
                'address': data['address'],
                'pincode': data['pincode'],
                'items' : data['items'],
                'date_created': data['date'],
                'fulfilled': False
            }
            CB_MARGAO.insert_one(new_order)
            return jsonify({'status': 'success', 'message': 'Form data saved successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Delivery not available for the entered pincode'}), 400
    
    else:
        return jsonify({'status': 'error', 'message': 'Invalid outlet selected'}), 400

