from flask import Blueprint, request, jsonify
import os
import uuid
from services.converter_factory import ConverterFactory
from werkzeug.utils import secure_filename
from utils.file_utils import allowed_file

convert_bp = Blueprint("convert", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    filename = secure_filename(file.filename)

    # Criar um diretório único para esta conversão
    conversion_id = str(uuid.uuid4())
    conversion_dir = os.path.join(UPLOAD_FOLDER, conversion_id)
    os.makedirs(conversion_dir, exist_ok=True)

    # Salvar o arquivo dentro do diretório único com seu nome original
    file_path = os.path.join(conversion_dir, filename)
    file.save(file_path)

    try:
        ext = os.path.splitext(filename)[1].lstrip(".").lower()
        converter = ConverterFactory.get_service(ext)
        output_file = converter.convert(file_path, to)

        return jsonify({
            "message": "Conversão realizada com sucesso",
            "output_file": output_file
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
