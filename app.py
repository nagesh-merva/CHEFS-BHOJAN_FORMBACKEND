from flask import Flask, render_template, request, make_response, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS
from email.message import EmailMessage
import os

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_secure_default_key')

CORS(app, supports_credentials=True, allow_headers="*", origins="*", methods=["OPTIONS", "POST"])
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


client = MongoClient(
    'mongodb+srv://crob0008:GYfLnhxdJgeiOTPO@chefsbhojan.oxsu9gm.mongodb.net/',
    connectTimeoutMS=30000, 
    socketTimeoutMS=None)
db = client['FORMDATACOLLECTION']
Details = db['CONTACTS']

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

