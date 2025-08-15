import os
import subprocess
from config import UPLOAD_FOLDER
from pdf2docx import Converter

class DocumentService:
    def __init__(self):
        # Estratégia específica para converter PDF para DOCX
        self._strategies = {
            ('pdf', 'docx'): self._convert_pdf_to_docx,
        }
        # Estratégia padrão para todas as outras conversões via LibreOffice
        self._default_strategy = self._convert_with_soffice

    def convert(self, input_path, output_format):
        """
        Converte o documento selecionando a estratégia correta (ferramenta)
        com base nos formatos de entrada e saída.
        """
        input_ext = os.path.splitext(input_path)[1].lstrip('.').lower()
        output_ext = output_format.lower()

        # Procura por uma estratégia específica (ex: pdf -> docx)
        strategy = self._strategies.get((input_ext, output_ext))
        
        if not strategy:
            # Se não encontrar, usa a estratégia padrão (soffice)
            strategy = self._default_strategy
        
        try:
            return strategy(input_path, output_ext)
        except Exception as e:
            # Captura exceções de qualquer uma das estratégias
            raise RuntimeError(f"Erro ao converter documento: {e}")

    def _convert_pdf_to_docx(self, input_path, output_format):
        """Usa a biblioteca pdf2docx para a conversão de PDF para DOCX."""
        filename = os.path.basename(input_path)
        output_filename = f"{os.path.splitext(filename)[0]}.{output_format}"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        # Executa a conversão com pdf2docx
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
        
        return output_path

    def _convert_with_soffice(self, input_path, output_format):
        """Usa o LibreOffice (soffice) para as conversões padrão."""
        output_dir = UPLOAD_FOLDER
        
        # Executa a conversão com soffice
        subprocess.run([
            "soffice", "--headless", "--convert-to", output_format,
            "--outdir", output_dir, input_path
        ], capture_output=True, text=True, check=True)

        # Retorna o caminho do arquivo convertido
        converted_file = f"{os.path.splitext(os.path.basename(input_path))[0]}.{output_format}"
        return os.path.join(output_dir, converted_file)