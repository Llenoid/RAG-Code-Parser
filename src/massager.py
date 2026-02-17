import pandas as pd  # ty:ignore[unresolved-import]
from pandas import DataFrame, Series  # ty:ignore[unresolved-import]

class DataMassager:
    def __init__(self, chunks: list[str]):
        self.chunks: list[str] = chunks
        self.df: DataFrame = pd.DataFrame()

    def to_dataframe(self):
        self.df = pd.DataFrame({"text": self.chunks})

    def clean(self):
        if self.df is None or self.df.empty:
            return 

        df: DataFrame = self.df # Type hinting for the linter
        if df.empty:
            return

        df["text"] = df["text"].astype(str).str.strip() # clean whitespace
        df = df.loc[df["text"].str.len() > 20].copy()
        df = df.reset_index(drop=True)
        self.df = df

    def add_metadata(self):
        if self.df is None or self.df.empty:
            return
            
        self.df["text"] = self.df["text"].astype(str)
        self.df["token_count"] = self.df["text"].str.split().str.len()
