from flask import Flask, request, jsonify
import os
import logging
from logging.handlers import RotatingFileHandler
import json

app = Flask(__name__)

app.config['WELCOME_MESSAGE'] = os.getenv('WELCOME_MESSAGE', 'Welcome to the custom app')
app.config['LOG_LEVEL'] = os.getenv('LOG_LEVEL', 'INFO')
app.config['PORT'] = int(os.getenv('PORT', 5000))

log_dir = '/app/logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=3)
handler.setLevel(app.config['LOG_LEVEL'])
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.logger.setLevel(app.config['LOG_LEVEL'])

@app.route('/')
def home():
    return app.config['WELCOME_MESSAGE'], 200

@app.route('/status')
def status():
    return jsonify({"status": "ok"})

@app.route('/log', methods=['POST'])
def log_message():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    app.logger.info(data['message'])
    return jsonify({"status": "logged"}), 200

@app.route('/logs')
def get_logs():
    try:
        with open(log_file, 'r') as f:
            logs = f.read()
        return logs, 200, {'Content-Type': 'text/plain'}
    except FileNotFoundError:
        return "No logs found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'])