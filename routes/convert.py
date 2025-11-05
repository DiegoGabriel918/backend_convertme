from flask import Blueprint, request, jsonify, send_file
import os
import io
from services.converter_factory import ConverterFactory
from services.image_service import ImageService # Import for type checking
from utils.file_utils import allowed_file

convert_bp = Blueprint("convert", __name__)

@convert_bp.route("/convert", methods=["POST"])
def convert_file():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files["file"]
    to = request.form.get("to")

    if not file or file.filename == "":
        return jsonify({"error": "Arquivo inválido"}), 400

    if not to:
        return jsonify({"error": "Formato de saída não especificado"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Tipo de arquivo não suportado"}), 400

    try:
        file_content = file.read()
        input_ext = os.path.splitext(file.filename)[1].lstrip('.').lower()

        # Get the correct service from the factory
        service = ConverterFactory.get_service(input_ext)

        # Call the convert method with the correct signature
        if isinstance(service, ImageService):
            # ImageService has a simpler signature: content, output_format
            result_content, output_filename = service.convert(file_content, to)
        else:
            # Other services need input_ext for temporary files: content, input_ext, output_format
            result_content, output_filename = service.convert(file_content, input_ext, to)

        # Send the in-memory result
        return send_file(
            io.BytesIO(result_content),
            as_attachment=True,
            download_name=output_filename
        )

    except Exception as e:
        # All services now raise detailed RuntimeErrors
        return jsonify({"error": str(e)}), 500