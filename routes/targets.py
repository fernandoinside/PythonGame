from flask import Blueprint, render_template, redirect, url_for, request, jsonify
import subprocess
from bson.objectid import ObjectId
from config import mongo
from routes.auth import login_required

targets_bp = Blueprint('targets', __name__)

@targets_bp.route('/add_target', methods=['POST'])
@login_required
def add_target():
    target = request.form.get('target')
    action = request.form.get('action')
    result = None

    if action == 'ping':
        result = subprocess.run(['ping', '-n', '4', target], capture_output=True, text=True).stdout
    elif action == 'whois':
        result = subprocess.run(['whois', target], capture_output=True, text=True).stdout
    elif action == 'tracert':
        result = subprocess.run(['tracert', target], capture_output=True, text=True).stdout
        # Process the tracert result and generate the graph
        mongo.db.targets.insert_one({'target': target, 'action': action, 'result': result})
    else:
        mongo.db.targets.insert_one({'target': target, 'action': action, 'result': result})
    
    return redirect(url_for('auth.home'))

@targets_bp.route('/target/<id>', methods=['GET'])
@login_required
def get_target(id):
    target = mongo.db.targets.find_one_or_404({'_id': ObjectId(id)})
    return jsonify(target)
