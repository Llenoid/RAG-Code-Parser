import pandas as pd
from pandas import DataFrame, Series

class DataMassager:
    def __init__(self, chunks: list[str]):
        self.chunks: list[str] = chunks
        self.df: DataFrame | None = None

    def to_dataframe(self):
        self.df = pd.DataFrame({"text": self.chunks})

    def clean(self):
        if not isinstance(self.df, DataFrame):
            return 

        df: DataFrame = self.df # Type hinting for the linter
        df["text"] = df["text"].str.strip() # clean whitespace
        df = df.loc[df["text"].str.len() > 20].copy()
        df = df.reset_index(drop=True)
        self.df = df

    def add_metadata(self):
        if not isinstance(self.df, DataFrame):
            return
        self.df["token_count"] = self.df["text"].str.split().str.len()
