from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Data storage file
DATA_FILE = 'contacts.json'

def load_contacts():
    """Load contacts from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_contacts(contacts):
    """Save contacts to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(contacts, f, indent=2)

@app.route('/')
def home():
    """Serve the main page"""
    return """
    <html>
        <head>
            <title>IT Website Backend</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .endpoint { background: #f4f4f4; padding: 10px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>IT Website Backend Server</h1>
                <p>Server is running successfully!</p>
                <div class="endpoint">
                    <strong>Available Endpoints:</strong>
                    <ul>
                        <li>GET /api/contacts - Get all contact messages</li>
                        <li>POST /api/contact - Submit a new contact message</li>
                        <li>GET /api/courses - Get available courses</li>
                    </ul>
                </div>
                <p>Check the browser console for frontend functionality.</p>
            </div>
        </body>
    </html>
    """

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create contact object
        contact = {
            'id': len(load_contacts()) + 1,
            'name': data['name'].strip(),
            'email': data['email'].strip(),
            'message': data['message'].strip(),
            'timestamp': datetime.now().isoformat(),
            'status': 'new'
        }
        
        # Save to file
        contacts = load_contacts()
        contacts.append(contact)
        save_contacts(contacts)
        
        print(f"New contact received: {contact['name']} - {contact['email']}")
        
        return jsonify({
            'success': True,
            'message': 'Contact form submitted successfully',
            'contact_id': contact['id']
        })
        
    except Exception as e:
        print(f"Error processing contact: {e}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get all contact messages"""
    try:
        contacts = load_contacts()
        return jsonify({
            'success': True,
            'contacts': contacts,
            'count': len(contacts)
        })
    except Exception as e:
        print(f"Error loading contacts: {e}")
        return jsonify({
            'error': 'Failed to load contacts'
        }), 500

@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Get available courses"""
    courses = [
        {
            'id': 1,
            'name': 'Programming',
            'description': 'Learn fundamental programming concepts',
            'duration': '12 weeks',
            'level': 'Beginner'
        },
        {
            'id': 2,
            'name': 'Web Development',
            'description': 'Build modern web applications',
            'duration': '16 weeks',
            'level': 'Intermediate'
        },
        {
            'id': 3,
            'name': 'Data Science',
            'description': 'Analyze and visualize data',
            'duration': '20 weeks',
            'level': 'Advanced'
        },
        {
            'id': 4,
            'name': 'Cyber Security',
            'description': 'Protect systems from cyber threats',
            'duration': '18 weeks',
            'level': 'Intermediate'
        }
    ]
    
    return jsonify({
        'success': True,
        'courses': courses
    })

@app.route('/api/search', methods=['GET'])
def search_content():
    """Search functionality"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({
            'error': 'No search query provided'
        }), 400
    
    # Mock search results - in real application, you'd search a database
    all_content = [
        {'type': 'course', 'title': 'Programming', 'description': 'Learn programming basics'},
        {'type': 'course', 'title': 'Web Development', 'description': 'Build websites and web apps'},
        {'type': 'section', 'title': 'About IT', 'description': 'Information about IT field'},
    ]
    
    results = [item for item in all_content 
              if query in item['title'].lower() or query in item['description'].lower()]
    
    return jsonify({
        'success': True,
        'query': query,
        'results': results,
        'count': len(results)
    })

if __name__ == '__main__':
    # Create data file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        save_contacts([])
    
    print("Starting IT Website Server...")
    print("Server will run on: http://localhost:5000")
    print("Make sure your frontend is pointing to this URL")
    
    app.run(debug=True, host='0.0.0.0', port=5000)