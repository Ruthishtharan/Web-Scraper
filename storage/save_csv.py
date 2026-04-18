import pandas as pd
import os


def save_csv(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    flat = [{k: (", ".join(v) if isinstance(v, list) else v) for k, v in item.items()} for item in data]
    df = pd.DataFrame(flat)
    df.to_csv(path, index=False)
    print(f"Saved CSV to {path}")