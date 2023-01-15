
import pandas as pd
from datetime import datetime
def conv_csv(f, t):
    read_file = pd.read_csv (f)
    read_file.to_csv (t + "data.csv", index=None)