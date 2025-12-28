import pandas as pd

def merge_dataframes_on_column(dfs: list[pd.DataFrame], column: str) -> pd.DataFrame:
    """Merges a list of DataFrames on a specified column."""
    from functools import reduce
    return reduce(lambda left, right: pd.merge(left, right, on=column), dfs)