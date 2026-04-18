def clean_data(data):
    cleaned = []

    for item in data:
        if not item:
            continue

        # Example cleaning
        for key in item:
            if isinstance(item[key], str):
                item[key] = item[key].strip()

        cleaned.append(item)

    return cleaned