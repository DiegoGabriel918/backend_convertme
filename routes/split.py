from flask import Blueprint, request, jsonify
import os
import uuid
from services.document_service import convert
from werkzeug.utils import secure_filename

split_bp = Blueprint("split", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@split_bp.route("/split", methods=["POST"])
def split_file():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files["file"]
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(file_path)

    start_page = request.form.get("start_page")
    end_page = request.form.get("end_page")

    if not start_page or not end_page:
        return jsonify({"error": "Informe página inicial e final"}), 400

    try:
        split_files = convert.split_document(file_path, int(start_page), int(end_page))
        return jsonify({
            "message": "Arquivo dividido com sucesso",
            "output_files": split_files
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
