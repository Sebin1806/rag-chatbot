import os

from app.services.pdf_service import PDFService
from app.services.docx_service import DOCXService
from app.services.txt_service import TXTService
from app.services.markdown_service import MarkdownService
from app.services.html_service import HTMLService
from app.services.ppt_service import PPTService
from app.services.excel_service import ExcelService
from app.services.csv_service import CSVService


class DocumentLoader:

    @staticmethod
    def load(file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            # Return list of pages
            return PDFService.extract_pages(file_path)

        elif extension == ".docx":
            return DOCXService.extract_text(file_path)

        elif extension == ".txt":
            return TXTService.extract_text(file_path)

        elif extension == ".md":
            return MarkdownService.extract_text(file_path)

        elif extension in [".html", ".htm"]:
            return HTMLService.extract_text(file_path)

        elif extension == ".pptx":
            return PPTService.extract_text(file_path)

        elif extension in [".xlsx", ".xls"]:
            return ExcelService.extract_text(file_path)

        elif extension == ".csv":
            return CSVService.extract_text(file_path)

        else:
            raise Exception(f"Unsupported file type: {extension}")