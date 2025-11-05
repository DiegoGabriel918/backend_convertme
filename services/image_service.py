import io
from PIL import Image

class ImageService:
    """Serviço para manipulação de imagens 100% em memória."""

    def __init__(self):
        self._strategies = {
            "pdf": self._convert_to_pdf,
            "jpg": self._convert_to_generic_image,
            "jpeg": self._convert_to_generic_image,
            "png": self._convert_to_generic_image,
            "webp": self._convert_to_generic_image,
            "bmp": self._convert_to_generic_image,
        }

    def convert(self, file_content, output_format):
        """Converte o conteúdo da imagem para o formato de saída desejado."""
        strategy = self._strategies.get(output_format.lower())
        if not strategy:
            raise ValueError(f"Conversão de imagem para o formato '{output_format}' não é suportada.")

        try:
            with Image.open(io.BytesIO(file_content)) as img:
                output_buffer = strategy(img, output_format)
            output_buffer.seek(0)
            return output_buffer.read(), f"converted.{output_format}"
        except Exception as e:
            raise RuntimeError(f"Erro ao converter imagem: {e}")

    def _convert_to_pdf(self, img, output_format):
        output_buffer = io.BytesIO()
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_buffer, "PDF", resolution=100.0)
        return output_buffer

    def _convert_to_generic_image(self, img, output_format):
        output_buffer = io.BytesIO()
        # Garante que imagens com transparência sejam tratadas para formatos como JPEG
        if img.mode in ('RGBA', 'P') and output_format.lower() in ('jpg', 'jpeg'):
            img = img.convert('RGB')
        img.save(output_buffer, format=output_format.upper())
        return output_buffer