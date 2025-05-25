import zipfile
import os 

def zip_folder(path_lists:list[str],out_file:str,rel_base:str,verbose:bool = False):
    with zipfile.ZipFile(out_file,"w",zipfile.ZIP_DEFLATED) as zip:
        for file in path_lists:
            rel_path = os.path.relpath(file,start=rel_base)
            if verbose:
                print(rel_path)
            zip.write(file,arcname=rel_path)
    print("Finished:")

def unzip(file:str,destinaton="."):
    with zipfile.ZipFile(file,"r") as zip:
        zip.extractall(destinaton)

