import subprocess
import json
import re
from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskwebapp"
mongo = PyMongo(app)

def run_network_scan(network):
    command = ['nmap', network]
    result = subprocess.run(command, capture_output=True, text=True).stdout

    devices = []
    current_device = None

    for line in result.splitlines():
        if line.startswith('Nmap scan report for'):
            if current_device:
                devices.append(current_device)
            ip = line.split()[-1]
            current_device = {'ip': ip, 'ports': [], 'mac': 'Unknown', 'os': 'Unknown'}
        elif 'MAC Address' in line:
            mac = line.split()[2]
            current_device['mac'] = mac
        elif re.match(r'\d+/tcp\s+\w+\s+\w+', line):
            parts = line.split()
            port_info = {'port': parts[0], 'state': parts[1], 'service': parts[2]}
            current_device['ports'].append(port_info)
        elif line.startswith('Host is up'):
            pass  # Skip this line

    if current_device:
        devices.append(current_device)

    with app.app_context():
        mongo.db.targets.insert_one({'target': network, 'action': 'network_scan', 'result': devices})

    return devices

if __name__ == "__main__":
    network = '192.168.3.0/24'  # Change this to your network
    devices = run_network_scan(network)
    print(json.dumps(devices, indent=4))
