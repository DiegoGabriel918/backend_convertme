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
    "mp3": ["wav"],
    "wav": ["mp3"],
    "ogg": ["mp3", "wav"],

    # Vídeo
    "mp4": ["mkv"],
    "mkv": ["mp4"]
}

FILE_TYPE_MAPPING = {
    "document": ["docx", "xlsx", "pptx", "pdf", "txt"],
    "image": ["jpg", "jpeg", "png", "gif", "bmp"],
    "audio": ["mp3", "wav"],
    "video": ["mp4", "avi", "mkv", "mov"]
}