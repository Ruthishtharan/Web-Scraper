import pandas as pd
import os


def save_excel(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)
    print(f"Saved Excel to {path}")
