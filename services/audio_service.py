import os
import subprocess
import uuid
import shutil

class AudioService:
    """Serviço para conversão de áudio usando FFmpeg com arquivos temporários."""

    def convert(self, file_content, input_ext, output_format):
        temp_dir = os.path.join("uploads", str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_input_path = os.path.join(temp_dir, f"input.{input_ext}")
        output_filename = f"output.{output_format}"
        temp_output_path = os.path.join(temp_dir, output_filename)

        try:
            with open(temp_input_path, 'wb') as f:
                f.write(file_content)

            command = ["ffmpeg", "-i", temp_input_path, temp_output_path]
            
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )

            with open(temp_output_path, 'rb') as f:
                result_content = f.read()
            
            return result_content, output_filename

        except FileNotFoundError:
            raise RuntimeError("Erro: 'ffmpeg' não encontrado. Verifique se está instalado e no PATH do sistema.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erro do FFmpeg ao converter áudio: {e.stderr}")
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
