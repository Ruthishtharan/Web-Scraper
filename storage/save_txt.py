import os


def save_txt(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for i, item in enumerate(data, 1):
            f.write(f"--- Record {i} ---\n")
            for key, value in item.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
    print(f"Saved TXT to {path}")
