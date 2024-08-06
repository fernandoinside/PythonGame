from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from functools import wraps
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import subprocess
import re
import json
import threading
import socket
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuração do MongoDB
app.config["MONGO_URI"] = "mongodb://mongodb:27017/mydatabase"
mongo = PyMongo(app)

# Dummy user data
users = {
    "fernando": "123456"
}

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def home():
    targets = mongo.db.targets.find()
    return render_template('dashboard.html', targets=targets)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))

@app.route('/add_target', methods=['POST'])
@login_required
def add_target():
    target = request.form.get('target')
    action = request.form.get('action')

    if action == 'network_scan':
        thread = threading.Thread(target=run_network_scan, args=(target,))
        thread.start()
    elif action == 'detailed_scan':
        thread = threading.Thread(target=run_detailed_scan, args=(target,))
        thread.start()

    mongo.db.targets.insert_one({'target': target, 'action': action, 'result': None})
    
    return redirect(url_for('home'))

@app.route('/scan_result/<id>', methods=['GET'])
@login_required
def get_scan_result(id):
    target = mongo.db.targets.find_one_or_404({'_id': ObjectId(id)})
    return jsonify(target)

@app.route('/last_scan', methods=['GET'])
@login_required
def get_last_scan():
    last_scan = mongo.db.targets.find().sort('_id', -1).limit(1)
    return jsonify({'scan_id': str(last_scan['_id'])})

@app.route('/scan_status/<id>', methods=['GET'])
@login_required
def get_scan_status(id):
    target = mongo.db.targets.find_one_or_404({'_id': ObjectId(id)})
    status = 'completed' if target['result'] is not None else 'pending'
    return jsonify({'status': status})

def run_network_scan(target):
    result = subprocess.run(['nmap', '-sn', target], capture_output=True, text=True).stdout
    parsed_result = parse_nmap_output(result)
    mongo.db.targets.update_one({'target': target}, {'$set': {'result': parsed_result}})

def run_detailed_scan(target):
    result = subprocess.run(['nmap','-T4', '-A', target], capture_output=True, text=True).stdout
    parsed_result = parse_detailed_nmap_output(result)
    mongo.db.targets.update_one({'target': target}, {'$set': {'result': parsed_result}})

def parse_nmap_output(output):
    # Parse the nmap output to extract relevant information
    # This is a simplified example, adjust it to match your nmap output
    devices = []
    for line in output.split('\n'):
        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
        if match:
            devices.append({'ip': match.group(1), 'os': 'Unknown'})
    return devices

def parse_detailed_nmap_output(output):
    # Parse the detailed nmap output to extract relevant information
    # This is a simplified example, adjust it to match your nmap output
    devices = []
    current_device = {}
    for line in output.split('\n'):
        ip_match = re.search(r'Nmap scan report for (.+)', line)
        port_match = re.search(r'(\d+/tcp)\s+(\w+)\s+(\w+)', line)
        mac_match = re.search(r'MAC Address: ([0-9A-F:]+)', line)
        if ip_match:
            if current_device:
                devices.append(current_device)
            current_device = {'ip': ip_match.group(1), 'ports': [], 'mac': 'Unknown', 'os': 'Unknown'}
        elif port_match:
            current_device['ports'].append({'port': port_match.group(1), 'state': port_match.group(2), 'service': port_match.group(3)})
        elif mac_match:
            current_device['mac'] = mac_match.group(1)
    if current_device:
        devices.append(current_device)
    return devices

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

if __name__ == '__main__':
    port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('0.0.0.0', port))
    if result == 0:
        port = find_free_port()
        print(f"Porta 5000 está em uso, usando a porta {port} em vez disso.")
    else:
        print(f"Usando a porta {port}")
    app.run(host='0.0.0.0', port=port)