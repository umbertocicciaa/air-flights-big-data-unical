import logging
from flask import Blueprint, Flask, app, request, jsonify
from services.etlservice import EtlService

etl_blueprint = Blueprint('etl', __name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

service = EtlService()

@etl_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.error("No file part in the request")
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    return service.convertFileToParquet(file)