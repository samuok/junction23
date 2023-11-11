import numpy as np
import pandas as pd
import os

def get_path(filename):
    """Returns an opened file object for the given filename and mode."""
    directory_path = os.path.dirname(os.path.realpath(__file__))
    file_path = directory_path+filename

    return file_path

def get_dataframe(filepath):
    df = pd.read_json(filepath)
    return df