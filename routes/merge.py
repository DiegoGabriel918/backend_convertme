from flask import Blueprint, request, jsonify
import os
import uuid
from services.document_service import DocumentService
from werkzeug.utils import secure_filename

merge_bp = Blueprint("merge", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@merge_bp.route("/merge", methods=["POST"])
def merge_files():
    files = request.files.getlist("files")

    if not files or len(files) < 2:
        return jsonify({"error": "Envie pelo menos dois arquivos"}), 400

    saved_paths = []
    for file in files:
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"
        path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(path)
        saved_paths.append(path)

    try:
        merged_file = DocumentService.merge_documents(saved_paths)
        return jsonify({
            "message": "Arquivos mesclados com sucesso",
            "output_file": merged_file
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
