from services.document_service import DocumentService
from services.image_service import ImageService
from services.audio_service import AudioService
from services.video_service import VideoService
from utils.constants import FILE_TYPE_MAPPING

# Mapeia a categoria ao serviço correspondente
SERVICE_MAPPING = {
    "document": DocumentService,
    "image": ImageService,
    "audio": AudioService,
    "video": VideoService,
}

# Cria um dicionário reverso para busca rápida (ex: "pdf" -> "document")
EXTENSION_TO_TYPE = {
    ext: file_type
    for file_type, extensions in FILE_TYPE_MAPPING.items()
    for ext in extensions
}

class ConverterFactory:
    """Factory para retornar o serviço correto com base no tipo de arquivo."""

    @staticmethod
    def get_service(file_extension):
        ext = file_extension.lower().lstrip(".")
        file_type = EXTENSION_TO_TYPE.get(ext)

        if file_type and file_type in SERVICE_MAPPING:
            # Retorna uma nova instância do serviço correto
            return SERVICE_MAPPING[file_type]()
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {ext}")