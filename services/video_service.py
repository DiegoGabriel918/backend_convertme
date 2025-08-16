import os
import subprocess

class VideoService:
    """Serviço para conversão de vídeos usando FFmpeg."""

    def convert(self, input_path, output_format):
        # O arquivo de saída deve ser salvo no mesmo diretório do arquivo de entrada
        input_dir = os.path.dirname(input_path)
        base_filename = os.path.basename(input_path)
        output_filename = f"{os.path.splitext(base_filename)[0]}.{output_format}"
        output_path = os.path.join(input_dir, output_filename)

        try:
            # Adicionado capture_output=True e text=True para obter detalhes do erro
            subprocess.run([
                "ffmpeg",
                "-i", input_path,
                output_path
            ], check=True, capture_output=True, text=True)
            return output_path
        except subprocess.CalledProcessError as e:
            # Levanta um erro com a saída de erro real do ffmpeg para depuração
            error_details = e.stderr if e.stderr else "Nenhum detalhe de erro do ffmpeg foi capturado."
            raise RuntimeError(f"Erro do FFmpeg ao converter vídeo: {error_details}")
