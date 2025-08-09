from services.document_service import convert
from services.image_service import ImageService
from services.audio_service import AudioService
from services.video_service import VideoService


class ConverterFactory:
    """Factory para retornar o serviço correto com base no tipo de arquivo."""

    @staticmethod
    def get_service(file_extension):
        # Remove ponto e deixa tudo minúsculo
        ext = file_extension.lower().lstrip(".")

        if ext in ["docx", "xlsx", "pptx", "pdf"]:
            return convert(input_path=file_extension, output_format=ext)
        elif ext in ["jpg", "jpeg", "png", "gif", "bmp"]:
            return ImageService()
        elif ext in ["mp3", "wav", "aac", "ogg"]:
            return AudioService()
        elif ext in ["mp4", "avi", "mkv", "mov"]:
            return VideoService()
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {ext}")

