import os
from repositories.etlrepository import EtlRepository
import logging
from flask import jsonify
from etl import etl_process


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EtlService:
    def __init__(self):
        self.repository = EtlRepository()

    def convertFileToParquet(self, file):
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({"error": "No selected file"}), 400
    
        if file and file.filename.endswith('.csv'):
            input_path = self.repository.createInputPath(file) 
            output_path = self.repository.createOutputPath(file)
            self.repository.saveFile(file,input_path)
            
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
