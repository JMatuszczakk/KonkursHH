from flask import Flask, request, jsonify
from datetime import datetime
import csv
import os
from pathlib import Path

app = Flask(__name__)

# CSV file configuration
CSV_FILE = 'voltage_readings_server.csv'
CSV_HEADERS = ['timestamp', 'device_id', 'raw_value', 'voltage']

def init_csv():
    """Initialize the CSV file if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)

def append_to_csv(data):
    """Append a new reading to the CSV file"""
    timestamp = datetime.now().isoformat()
    row = [
        timestamp,
        data['device_id'],
        data['raw_value'],
        data['voltage']
    ]
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

def read_csv_data(device_id=None, limit=100):
    """Read data from CSV file with optional device_id filter"""
    readings = []
    try:
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if device_id is None or row['device_id'] == device_id:
                    readings.append(row)
    except FileNotFoundError:
        return []
    
    # Sort by timestamp in descending order and apply limit
    readings.sort(key=lambda x: x['timestamp'], reverse=True)
    return readings[:limit]

@app.before_first_request
def setup():
    """Run setup before first request"""
    init_csv()

@app.route('/voltage', methods=['POST'])
def receive_voltage():
    """Receive voltage readings from ESP devices"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['device_id', 'raw_value', 'voltage']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Store in CSV
        append_to_csv(data)
        
        return jsonify({
            'status': 'success',
            'message': 'Voltage reading stored',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/voltage/<device_id>', methods=['GET'])
def get_voltage_history(device_id):
    """Get voltage history for a specific device"""
    try:
        limit = request.args.get('limit', default=100, type=int)
        readings = read_csv_data(device_id=device_id, limit=limit)
        return jsonify(readings)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/voltage/latest', methods=['GET'])
def get_latest_readings():
    """Get latest reading for all devices"""
    try:
        # Read all readings
        all_readings = read_csv_data()
        
        # Group by device_id and get latest reading for each
        latest_readings = {}
        for reading in all_readings:
            device_id = reading['device_id']
            if device_id not in latest_readings:
                latest_readings[device_id] = reading
        
        return jsonify(list(latest_readings.values()))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/voltage/download', methods=['GET'])
def download_csv():
    """Download the entire CSV file"""
    try:
        return send_file(
            CSV_FILE,
            mimetype='text/csv',
            as_attachment=True,
            download_name='voltage_readings.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure CSV file is initialized
    init_csv()
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
