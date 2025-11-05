from flask import Blueprint, request, jsonify, send_file
import io
from services.document_service import DocumentService

merge_bp = Blueprint("merge", __name__)

@merge_bp.route("/merge", methods=["POST"])
def merge_files():
    files = request.files.getlist("files")

    if not files or len(files) < 2:
        return jsonify({"error": "Envie pelo menos dois arquivos para juntar."}), 400

    try:
        file_contents = []
        for file in files:
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({"error": "A função de juntar arquivos suporta apenas arquivos PDF."}), 400
            file_contents.append(file.read())

        # Call the in-memory service
        merged_content = DocumentService.merge_documents(file_contents)

        # Send the in-memory merged PDF
        return send_file(
            io.BytesIO(merged_content),
            as_attachment=True,
            download_name="merged.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500