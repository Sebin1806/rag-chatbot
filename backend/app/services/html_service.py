from bs4 import BeautifulSoup


class HTMLService:

    @staticmethod
    def extract_text(file_path):

        with open(file_path, "r", encoding="utf-8") as file:
            html = file.read()

        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(separator="\n")