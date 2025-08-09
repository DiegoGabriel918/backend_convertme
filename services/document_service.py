import os
import subprocess
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER

import subprocess

def convert(input_path, output_format):
    output_path = UPLOAD_FOLDER
    try:
        result = subprocess.run([
            "soffice",
            "--headless",
            "--convert-to", output_format,
            "--outdir", output_path,
            input_path
        ], capture_output=True, text=True, check=True)

        print("stdout:", result.stdout)
        print("stderr:", result.stderr)

        converted_file = os.path.splitext(os.path.basename(input_path))[0] + f".{output_format}"
        return os.path.join(output_path, converted_file)

    except subprocess.CalledProcessError as e:
        print("Erro:", e.stderr)
        raise RuntimeError(f"Erro ao converter documento: {e.stderr}")


    def merge(self, files):
        raise NotImplementedError("Merge de documentos ainda não implementado.")

    def split(self, file, pages):
        raise NotImplementedError("Split de documentos ainda não implementado.")
