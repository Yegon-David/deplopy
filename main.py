# from src.file import get_file_structure
# from src.zip import zip_folder,unzip
from src.depends import install_db,install_app,install_server,install_proxy
from config import STATE_FILE

from pprint import pprint
import json


def load(file=STATE_FILE):
    with open(file,"r",encoding="utf-8") as f:
        return json.load(f)

def write(data,file=STATE_FILE):
    with open(file,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4)


def main():
    # path = "/home/yegon/projects/python/deplo/.venv/lib/"
    # files = get_file_structure(path)
    # zip_folder(files,"test.zip",path)
    # unzip("test.zip","./tee")
    state = load()
    P_DIR = state["destination"]
    if not state["db"]["done"]:
        install_db(state["db"])
    if not state["app"]["done"]:
        install_app(state)
    if not state["server"]["done"]:
        install_server(state)
    if not state["server"]["done"]:
        install_proxy(state)

    


if __name__ == "__main__":
    main()
