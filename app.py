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

MONGODB_URI = os.getenv('MONGODB_URI')
if not MONGODB_URI:
    raise ValueError("Missing MONGODB_URI environment variable")

client = MongoClient(
    MONGODB_URI,
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
    
    existing_contact = Details.find_one({
        '$or': [
            {'name': data['name']},
            {'phone': data['phone']}
        ]
    })
    
    if existing_contact:
        print('data not added')
        return jsonify({'status': 'exists', 'message': 'Contact already exists, Try asking your Fam and Friends to get more Discount'}), 200
    
    new_contact = {
        'name': data['name'],
        'phone': data['phone'],
        'date_created': datetime.utcnow()
    }
    print('data added')
    Details.insert_one(new_contact)
    print(data)
    
    return jsonify({'status': 'success', 'message': 'Form data saved successfully'}), 200

