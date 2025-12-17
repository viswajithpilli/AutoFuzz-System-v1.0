from flask import Flask, request, jsonify, send_from_directory
from fuzzer import Fuzzer
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/fuzz', methods=['POST'])
def fuzz_api():
    data = request.json
    binary_path = data.get('binary_path')
    
    if not binary_path or not os.path.exists(binary_path):
        return jsonify({'error': 'Invalid binary path'}), 400
        
    fuzzer = Fuzzer(binary_path)
    result = fuzzer.fuzz()
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
