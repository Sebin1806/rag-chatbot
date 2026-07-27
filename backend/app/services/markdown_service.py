import markdown
from bs4 import BeautifulSoup


class MarkdownService:

    @staticmethod
    def extract_text(file_path):

        with open(file_path, "r", encoding="utf-8") as file:
            md_content = file.read()

        html = markdown.markdown(md_content)

        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(separator="\n")