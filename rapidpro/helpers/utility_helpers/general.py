import pandas as pd

def is_not_empty(dataframe):
    if dataframe is not None and len(dataframe.index) > 0:
        return True
    else:
        return False
