import os
import shutil
import uuid

def save_uploaded_file(file, upload_folder):
    """Salva um arquivo enviado para o diretório definido."""
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return filepath

def move_file(src, dest_folder):
    """Move um arquivo para outro diretório."""
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest_path = os.path.join(dest_folder, os.path.basename(src))
    shutil.move(src, dest_path)
    return dest_path

def delete_file(filepath):
    """Remove um arquivo se ele existir."""
    if os.path.exists(filepath):
        os.remove(filepath)

def clear_folder(folder_path):
    """Remove todos os arquivos de uma pasta."""
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
