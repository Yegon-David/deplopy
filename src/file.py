import os

EX = [
    ".git",
    "ref",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "db.sqlite3",
    "static",
    ".session.vim",
]

def get_file_structure(path: str, result:list[str]=[]) -> list:
    for obj in os.listdir(path):
        if obj in EX:
            print(f"IGNORING: {obj}")
            continue

        full = os.path.join(path, obj)
        if not os.path.isdir(full):
            result.append(full)

        else:
            get_file_structure(full)
    return result