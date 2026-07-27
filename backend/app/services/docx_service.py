from docx import Document


class DOCXService:

    @staticmethod
    def extract_text(file_path):

        document = Document(file_path)

        text = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)

        return "\n".join(text)