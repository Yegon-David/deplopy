import subprocess as sp 
import time
import shutil
from config import DB,os,ENV
from .setup import WAITRESS,NGINX_BASE_CONFIG,NGINX_APP_CONF,NGINX_SERVICE
from src.zip import unzip

command = f'''
create database if not exists {DB["name"]};
create user if not exists '{DB["user"]}'@'localhost' identified by '{DB["password"]}';
grant all privileges on {DB["name"]}.* to '{DB["user"]}'@'localhost';
flush privileges;
'''

def db(path):
    print("Install mariadb:")
    start = time.time()
    proc = sp.run(["powershell","-Command","msiexec","/i",path],shell=True)
    print("completed in",round(time.time()-start,2))

def test(state):
    ex = state["bin"]
    if not ex:
        print("binary not loaded")
        "TODO: search for binary"
        return False 
    print("Running mysql")
    proc = sp.run([ex,"-uroot",f"-pyegon1234"],input=command,text=True,capture_output=True)
    # proc = sp.run([ex,"-usamoa","-psamoa1234"],
    # input='''
    # create table if not exists test (
    # name varchar(55)
    # )
    # ''',text=True,capture_output=True
    # )
    if not proc.returncode == 0:
        print("done:",proc.returncode)
        print("error",proc.stderr)
        print("success",proc.stdout)
        return False
    return True
    
def install_db(state):
    print("Running")
    if not state["install"]:
        db("F:\\projects\\deplopy\\test\\tools\\mariadb-11.7.2-winx64.msi")
    print("Database is already installed.")
    if not state["tested"]:
        ok = test(state)
        if ok:
            print("user creation success")
            state["tested"]=True
        else:
            print("test failed")

def install_app(state):
    project = state['project']
    dst = state["destination"]
    app = state["app"]
    b_dir = os.path.join(dst,project)
    zipfile = "app1.zip"
    load = app["loaded"]
    if not load:
        if not os.path.isfile(zipfile):
            raise FileNotFoundError
        if not os.path.isdir(dst):
            os.makedirs(dst,exist_ok=True)

        print("unzipping",project)
        unzip(zipfile,b_dir)
        print("Unzipping complete")
        with open(os.path.join(b_dir,".env.prod"),"w",encoding="utf-8") as ev:
            ev.write(ENV.format(user=DB["user"],password=DB["password"],database=DB["name"]))
            print("Env file loaded")
    
    original = os.getcwd()
    os.chdir(b_dir)
    proc = sp.run(["powershell","-Command","uv","sync"],capture_output=True,text=True)
    if proc.returncode != 0:
        print("error:\n",proc.stderr)
        return
    proc2 = sp.run(["powershell","-Command","uv","run","manage.py","check"],capture_output=True,text=True)
    if proc2.returncode != 0:
        print("error in check:\n",proc2.stderr)
        return
    print("done",proc2.stdout)
    os.chdir(original)

def load_waitress(state):
    app_name = state["project"]
    path= state["destination"]
    asrv = state["server"]["app_server"]

    fp = os.path.join(path,"config")
    if not os.path.exists(fp):
        os.makedirs(fp,exist_ok=True)
    conf_name = f"winsw_{app_name}.xml"
    winsw_file = f"winsw_{app_name}.exe"
    winsw_exe = os.path.join(fp,winsw_file)
    conf_file = os.path.join(fp,conf_name)

    if not asrv["loaded"]:
        print("Loading waitress: ")
        config = WAITRESS.format(project=app_name,path=os.path.join(path,app_name))
       

        src = "./depends/winsw.exe"

        with open(os.path.join(fp,conf_file),"w",encoding="utf-8") as f:
            f.write(config)
            print("waitress loaded")

    
    if not os.path.exists(winsw_exe):
        shutil.copy(src,dst=winsw_exe)
        print("copying success")
    
    if not asrv["installed"]:
        print("installing waitress")
        proc = sp.run(["powershell","-Command",winsw_exe,"install"],cwd=fp,text=True,capture_output=True)
        if proc.returncode != 0:
            print("Failed to install winsw")
            print(proc.stderr)
            return
        print("success\n",proc.stdout)
    
    print("Testing Server")
    pr = sp.run(["powershell","-Command",winsw_exe,"status"],cwd=fp,capture_output=True,text=True)
    if pr.returncode:
        print("Error in server test",pr.stderr)
        return
    print(pr.stdout)
    
def install_server(state):
    print("Starting server installation:")
    ngnxzip="nginx.zip"
    dst = state["destination"]
    srv = state["server"]
    if not srv["loaded"]:
        unzip(ngnxzip,dst)
        
    def rename_ngnx(fd):
        print("Renaming")
        found=False
        for folder in os.listdir(fd):
            fll=os.path.join(fd,folder)
            if "nginx" in folder and os.path.isdir(fll):
                os.rename(fll,os.path.join(dst,"nginx"))
                print("rename success")
                found=True
                return
        if not found:
            print("rename failed")
            raise FileNotFoundError
    if not srv["renamed"]:
        rename_ngnx(dst)
    
    if not srv["app_server"]["done"]:
        load_waitress(state)
    print("success")

def install_proxy(state):
    print("started nginx loading")
     
    path = state["destination"]
    cfd = os.path.join(path,"config")
    srv = state["server"]["nginx_server"]
    
    if not os.path.exists(cfd):
        os.makedirs(cfd)
    config_name = f"{state["project"]}.conf"

    conf = os.path.join(cfd,config_name)
    conf_xml_file = os.path.join(cfd,"winsw_nginx.xml") 
    conf_exe_file = os.path.join(cfd,"winsw_nginx.exe")
    
    if not srv["loaded"]:
        with open(conf,"w",encoding="utf-8") as f:
            f.write(NGINX_APP_CONF.format(base_dir=os.path.join(path,state["project"]).replace("\\","/")))
        with open(os.path.join(path,"nginx","conf","nginx.conf"),"w",encoding="utf-8") as f:
            f.write(NGINX_BASE_CONFIG.format(custom_config_path=conf.replace("\\","/")))
        
        with open(conf_xml_file,"w",encoding="utf-8") as f:
            nginx_fd = os.path.join(path,"nginx")
            f.write(NGINX_SERVICE.format(
                    path=nginx_fd.replace("/","\\"),
                    exe_file=os.path.join(nginx_fd,"nginx.exe").replace("/","\\"),
                    base_dir=os.path.join(path,state["project"]).replace("/","\\"))
                    )

        if not os.path.exists(conf_exe_file):
            exist_exe = os.path.join(cfd,f"winsw_{state["project"]}.exe")
            if os.path.exists(exist_exe):
                shutil.copy(exist_exe,conf_exe_file)
                print("winsw copied successfully")
            else:
                #TODO :copy from actual source
                print("No exe file found")
                return
                
    if not srv["installed"]:  
        print("Installing")
        proc=sp.run(["powershell","-Command",conf_exe_file,"install"],text=True,capture_output=True)
        if proc.returncode != 0:
            print("error",proc.stderr)
        print("done",proc.stdout)

    if not srv["done"]:
        print("Testing if it works")
        proc=sp.run(["powershell","-Command",conf_exe_file,"status"],text=True,capture_output=True)
        if proc.returncode != 0:
            print("error",proc.stderr)
        out = proc.stdout.strip() 
        print("len",len(out))
        print("out",out)
        if out.lower() != "started":
            print("will restart!")
            procs=sp.run(["powershell","-Command",conf_exe_file,"restart"],text=True,capture_output=True)
            if procs.returncode != 0:
                print("error in restarting:",procs.stderr)
            
