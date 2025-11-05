import os
import subprocess
import uuid
import io
import zipfile
from pdf2docx import Converter
import fitz  # PyMuPDF

class DocumentService:
    def __init__(self):
        self._strategies = {
            ('pdf', 'docx'): self._convert_pdf_to_docx_in_memory,
        }
        self._default_strategy = self._convert_with_soffice_on_disk

    def convert(self, file_content, input_ext, output_format):
        output_ext = output_format.lower()
        strategy = self._strategies.get((input_ext, output_ext), self._default_strategy)
        
        try:
            # Pass content to in-memory strategies, or use disk for soffice
            if strategy == self._convert_with_soffice_on_disk:
                return strategy(file_content, input_ext, output_ext)
            else:
                return strategy(file_content, output_format)
        except Exception as e:
            raise RuntimeError(f"Erro ao converter documento: {e}")

    def _convert_pdf_to_docx_in_memory(self, file_content, output_format):
        output_buffer = io.BytesIO()
        cv = Converter(stream=io.BytesIO(file_content))
        cv.convert(docx_stream=output_buffer)
        cv.close()
        output_buffer.seek(0)
        return output_buffer.read(), f"converted.{output_format}"

    def _convert_with_soffice_on_disk(self, file_content, input_ext, output_format):
        temp_dir = os.path.join("uploads", str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_input_path = os.path.join(temp_dir, f"input.{input_ext}")
        
        try:
            with open(temp_input_path, 'wb') as f:
                f.write(file_content)

            subprocess.run([
                "soffice", "--headless", "--convert-to", output_format,
                "--outdir", temp_dir, temp_input_path
            ], capture_output=True, text=True, check=True)

            output_filename = f"input.{output_format}"
            converted_file_path = os.path.join(temp_dir, output_filename)
            
            with open(converted_file_path, 'rb') as f:
                result_content = f.read()
            
            return result_content, output_filename
        finally:
            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)

    @staticmethod
    def merge_documents(file_contents):
        from PyPDF2 import PdfWriter
        merger = PdfWriter()
        for content in file_contents:
            merger.append(io.BytesIO(content))
        
        output_buffer = io.BytesIO()
        merger.write(output_buffer)
        merger.close()
        output_buffer.seek(0)
        return output_buffer.read()

    @staticmethod
    def _parse_pages(pages_str, max_pages):
        # This helper function remains the same
        pages_to_extract = set()
        for part in pages_str.split(','):
            part = part.strip()
            if not part: continue
            if '-' in part:
                start, end = part.split('-')
                start = int(start)
                end = int(end)
                if start > end:
                    raise ValueError(f"Intervalo de páginas inválido: {start}-{end}")
                for i in range(start, end + 1):
                    if 1 <= i <= max_pages:
                        pages_to_extract.add(i)
            else:
                page = int(part)
                if 1 <= page <= max_pages:
                    pages_to_extract.add(page)
        return sorted(list(pages_to_extract))

    @staticmethod
    def split_document(file_content, options):
        doc = fitz.open(stream=file_content, filetype="pdf")
        zip_buffer = io.BytesIO()

        method = options.get("method")

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if method == "pages":
                pages_str = options.get("pages", "")
                if not pages_str: raise ValueError("Nenhuma página selecionada")
                pages_to_extract = DocumentService._parse_pages(pages_str, doc.page_count)
                for page_num in pages_to_extract:
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=page_num - 1, to_page=page_num - 1)
                    pdf_bytes = new_doc.write()
                    zipf.writestr(f"page_{page_num}.pdf", pdf_bytes)
                    new_doc.close()

            elif method == "fixed":
                interval = int(options.get("interval", 1))
                if interval <= 0: raise ValueError("Intervalo deve ser positivo")
                for i in range(0, doc.page_count, interval):
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=i, to_page=min(i + interval - 1, doc.page_count - 1))
                    pdf_bytes = new_doc.write()
                    zipf.writestr(f"split_{i//interval+1}.pdf", pdf_bytes)
                    new_doc.close()
            
            elif method == "extract":
                ranges = options.get("ranges", [])
                if not ranges: raise ValueError("Nenhum grupo de extração fornecido")
                
                for i, pages_str in enumerate(ranges):
                    if not pages_str.strip(): continue
                    
                    pages_to_extract = DocumentService._parse_pages(pages_str, doc.page_count)
                    if not pages_to_extract: continue

                    new_doc = fitz.open()
                    for page_num in pages_to_extract:
                        new_doc.insert_pdf(doc, from_page=page_num - 1, to_page=page_num - 1)
                    
                    pdf_bytes = new_doc.write()
                    zipf.writestr(f"group_{i+1}_pages_{pages_str.replace(',', '_')}.pdf", pdf_bytes)
                    new_doc.close()

            else:
                doc.close()
                raise ValueError(f"Método de divisão desconhecido: {method}")

        doc.close()
        zip_buffer.seek(0)
        return zip_buffer.read()
