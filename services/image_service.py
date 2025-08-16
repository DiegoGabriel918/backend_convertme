import os
from PIL import Image

class ImageService:
    """Serviço para manipulação de imagens usando o padrão Strategy."""

    def __init__(self):
        # Dicionário que mapeia o formato de saída para o método correto
        self._strategies = {
            "pdf": self._convert_to_pdf,
            "jpg": self._convert_to_generic_image,
            "jpeg": self._convert_to_generic_image,
            "png": self._convert_to_generic_image,
            "webp": self._convert_to_generic_image,
            "bmp": self._convert_to_generic_image,
        }

    def convert(self, input_path, output_format):
        """
        Converte a imagem para o formato de saída desejado.
        Usa um dicionário de 'strategies' para escolher o método de conversão.
        """
        input_dir = os.path.dirname(input_path)
        base_filename = os.path.basename(input_path)
        output_filename = f"{os.path.splitext(base_filename)[0]}.{output_format}"
        output_path = os.path.join(input_dir, output_filename)
        
        # Seleciona a estratégia com base no formato de saída
        strategy = self._strategies.get(output_format.lower())

        if not strategy:
            raise ValueError(f"Conversão de imagem para o formato '{output_format}' não é suportada.")

        try:
            with Image.open(input_path) as img:
                strategy(img, output_path) # Executa a estratégia
            return output_path
        except Exception as e:
            raise RuntimeError(f"Erro ao converter imagem: {e}")

    def _convert_to_pdf(self, img, output_path):
        """Estratégia específica para converter uma imagem para PDF."""
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_path, "PDF", resolution=100.0)

    def _convert_to_generic_image(self, img, output_path):
        """Estratégia genérica para salvar em outros formatos de imagem."""
        # Garante que imagens com transparência sejam tratadas para formatos como JPEG
        if img.mode in ('RGBA', 'P') and output_path.lower().endswith(('jpg', 'jpeg')):
            img = img.convert('RGB')
        img.save(output_path)
