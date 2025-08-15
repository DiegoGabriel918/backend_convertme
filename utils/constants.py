# Pares de conversão recíprocos e flexíveis
SUPPORTED_CONVERSIONS = {
    # Documentos
    "pdf": ["docx", "pptx", "xlsx", "txt"],
    "docx": ["pdf", "txt"],
    "pptx": ["pdf"],
    "xlsx": ["pdf"],
    "txt": ["pdf", "docx"],

    # Imagens
    "jpg": ["png", "webp", "pdf"],
    "jpeg": ["png", "webp", "pdf"],
    "png": ["jpg", "webp", "pdf"],
    "webp": ["jpg", "png", "pdf"],

    # Áudio
    "mp3": ["wav", "ogg"],
    "wav": ["mp3", "ogg"],
    "ogg": ["mp3", "wav"],

    # Vídeo
    "mp4": ["avi", "mov", "mkv"],
    "avi": ["mp4", "mov", "mkv"],
    "mov": ["mp4", "avi", "mkv"],
    "mkv": ["mp4", "avi", "mov"]
}

FILE_TYPE_MAPPING = {
    "document": ["docx", "xlsx", "pptx", "pdf", "txt"],
    "image": ["jpg", "jpeg", "png", "gif", "bmp"],
    "audio": ["mp3", "wav", "aac", "ogg"],
    "video": ["mp4", "avi", "mkv", "mov"]
}