import os
from PIL import Image
from config import UPLOAD_FOLDER

class ImageService:
    """Serviço para manipulação de imagens."""

    def convert(self, input_path, output_format):
        filename = os.path.basename(input_path)
        output_filename = os.path.splitext(filename)[0] + f".{output_format}"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)

        try:
            with Image.open(input_path) as img:
                if output_format.lower() == "pdf":
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(output_path, "PDF")
                else:
                    img.save(output_path, output_format.upper())
            return output_path
        except Exception as e:
            raise RuntimeError(f"Erro ao converter imagem: {e}")
