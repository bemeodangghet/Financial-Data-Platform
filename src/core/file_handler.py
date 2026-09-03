import os
import pandas as pd
from datetime import datetime

#dataframe to csv file
def save_csv(df: pd.DataFrame, file_path: str,) -> None:   
    # Tạo folder nếu chưa tồn tại
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    df.to_csv(file_path, index=False)

