import os
import subprocess

class AudioService:
    """Serviço para conversão de áudio usando FFmpeg."""

    def convert(self, input_path, output_format):
        # O arquivo de saída deve ser salvo no mesmo diretório do arquivo de entrada
        input_dir = os.path.dirname(input_path)
        base_filename = os.path.basename(input_path)
        output_filename = f"{os.path.splitext(base_filename)[0]}.{output_format}"
        output_path = os.path.join(input_dir, output_filename)

        command = ["ffmpeg", "-i", input_path, output_path]
        print(f"Executing command: ", ' '.join(command))

        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            print(f"FFmpeg stdout: {result.stdout}")
            print(f"FFmpeg stderr: {result.stderr}")
            return output_path
        except FileNotFoundError as e:
            raise RuntimeError(f"Erro: 'ffmpeg' não encontrado. Verifique se está instalado e no PATH do sistema. {e}")
        except subprocess.CalledProcessError as e:
            error_message = f"Erro ao converter áudio: {e}\n"
            error_message += f"FFmpeg stderr: {e.stderr}\n"
            error_message += f"FFmpeg stdout: {e.stdout}"
            raise RuntimeError(error_message)
        except Exception as e:
            raise RuntimeError(f"Um erro inesperado ocorreu: {e}")