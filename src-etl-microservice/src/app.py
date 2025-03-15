from flask import Flask, request, jsonify, send_file
import os
from etl import etl_process

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.csv'):
        input_path = os.path.join('/tmp', file.filename)
        output_path = os.path.join('/output/')
        file.save(input_path)
        
        etl_process(input_path, output_path)
        
        return jsonify({"message": "File converted successfully", "output_file": output_path}), 200
    
    return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)