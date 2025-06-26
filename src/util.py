import json

def parse_json(path_to_file: str) -> dict:
    with open(path_to_file,"r") as f:
        data = json.load(f)
    if f:
        f.close()
    return data

def dollar_format(x: int | float) -> str:
    if x < 0:
        return f"-${abs(x):,.2f}"
    else:
        return f"${x:,.2f}"
