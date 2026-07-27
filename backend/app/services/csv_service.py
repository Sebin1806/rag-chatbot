import pandas as pd


class CSVService:

    @staticmethod
    def extract_text(file_path):

        df = pd.read_csv(file_path)

        return df.to_string(index=False)