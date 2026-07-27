import pandas as pd


class ExcelService:

    @staticmethod
    def extract_text(file_path):

        excel = pd.ExcelFile(file_path)

        text = []

        for sheet in excel.sheet_names:

            df = pd.read_excel(file_path, sheet_name=sheet)

            text.append(f"Sheet: {sheet}")

            text.append(df.to_string(index=False))

        return "\n".join(text)