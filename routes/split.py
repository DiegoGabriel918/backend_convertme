from flask import Blueprint, request, jsonify, send_file
import json
import io
from services.document_service import DocumentService

split_bp = Blueprint("split", __name__)

@split_bp.route("/split", methods=["POST"])
def split_file():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "Nome de arquivo vazio"}), 400

    options_str = request.form.get("options")
    if not options_str:
        return jsonify({"error": "Opções de divisão não fornecidas"}), 400

    try:
        options = json.loads(options_str)
        file_content = file.read()

        # Call the in-memory service
        zipped_files_content = DocumentService.split_document(file_content, options)

        # Send the in-memory zip file
        return send_file(
            io.BytesIO(zipped_files_content),
            as_attachment=True,
            download_name="split_files.zip",
            mimetype='application/zip'
        )

    except Exception as e:
        # The service layer will raise specific errors
        return jsonify({"error": str(e)}), 500
