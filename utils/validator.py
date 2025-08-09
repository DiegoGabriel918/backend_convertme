import os
from utils.constants import SUPPORTED_CONVERSIONS

def is_allowed_file(filename):
    """Verifica se a extensão do arquivo é suportada."""
    ext = os.path.splitext(filename)[1].lower().replace(".", "")
    for src, targets in SUPPORTED_CONVERSIONS.items():
        if ext == src or ext in targets:
            return True
    return False

def validate_conversion(input_ext, output_ext):
    """Valida se a conversão solicitada é suportada."""
    input_ext = input_ext.lower()
    output_ext = output_ext.lower()

    if input_ext in SUPPORTED_CONVERSIONS:
        return output_ext in SUPPORTED_CONVERSIONS[input_ext]
    return False

def get_file_extension(filename):
    """Retorna a extensão de um arquivo sem o ponto."""
    return os.path.splitext(filename)[1].lower().replace(".", "")
