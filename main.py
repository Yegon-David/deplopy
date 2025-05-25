from src.file import get_file_structure
from src.zip import zip_folder,unzip

from pprint import pprint

def main():
    path = "/home/yegon/projects/python/deplo/.venv/lib/"
    files = get_file_structure(path)
    zip_folder(files,"test.zip",path)
    # unzip("test.zip","./tee")


if __name__ == "__main__":
    main()
