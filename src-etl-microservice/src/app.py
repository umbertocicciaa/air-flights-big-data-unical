from flask import Flask, request, jsonify, send_file
import os
import logging
from etl import etl_process

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.error("No file part in the request")
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.csv'):
        input_path = os.path.join('/tmp', file.filename)
        output_path = os.path.join('/mnt/shared-filesystem/outputs/', file.filename)
        file.save(input_path)
        
        logger.info(f"File saved to {input_path}")
        
        try:
            etl_process(input_path, output_path)
            logger.info(f"File processed successfully, output saved to {output_path}")
            return jsonify({"message": "File converted successfully", "output_file": output_path}), 200
        except Exception as e:
            logger.error(f"ETL process failed: {e}")
            return jsonify({"error": "ETL process failed"}), 500
    
    logger.error("Invalid file format. Please upload a CSV file.")
    return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)