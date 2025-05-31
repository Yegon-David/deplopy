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
    try:
        with zipfile.ZipFile(file,"r") as zip:
            zip.extractall(destinaton)
    except Exception as e:
        print("Unzipping error:",str(e))


if __name__ == "__main__":
    def zip_django(base_dir):
        from file import get_file_structure
        files = get_file_structure(base_dir)
        zip_folder(files,"app1.zip",base_dir)
    
    zip_django("F:\\projects\\deplopy\\test\\app1")


