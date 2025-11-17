import pandas as pd

def load_mtcars(path: str = "data/mtcars.csv") -> pd.DataFrame:
    return pd.read_csv(path)