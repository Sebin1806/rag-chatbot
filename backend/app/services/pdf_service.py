from pypdf import PdfReader


class PDFService:

    @staticmethod
    def extract_text(file_path: str) -> str:

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    @staticmethod
    def extract_pages(file_path: str):

        reader = PdfReader(file_path)

        pages = []

        print(f"\nTotal PDF Pages: {len(reader.pages)}")

        for page_number, page in enumerate(reader.pages, start=1):

            page_text = page.extract_text()
            print("\n========== PAGE TEXT ==========")
            print(page_text[:1500])
            print("===============================\n")

            if page_text:

                print(
                    f"Page {page_number} -> {len(page_text)} characters"
                )

                pages.append({
                    "page": page_number,
                    "text": page_text
                })

        return pages