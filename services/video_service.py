import os
import subprocess
from config import UPLOAD_FOLDER

class VideoService:
    """Serviço para conversão de vídeos usando FFmpeg."""

    def convert(self, input_path, output_format):
        filename = os.path.basename(input_path)
        output_filename = os.path.splitext(filename)[0] + f".{output_format}"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)

        try:
            subprocess.run([
                "ffmpeg",
                "-i", input_path,
                output_path
            ], check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erro ao converter vídeo: {e}")
