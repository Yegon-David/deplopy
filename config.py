import os 
from dotenv import load_dotenv

load_dotenv(".env")

STATE_FILE = "state.json"

INSTITUTION = "kabsabet"

DB = {
    "user":f"{INSTITUTION}_{os.getenv("DB_USER")}",
    "password": f"{INSTITUTION}_{os.getenv("DB_PASSWORD")}",
    "name":f"{INSTITUTION}_{os.getenv("DB_DATABASE")}",
}
ENV = '''
DEBUG=0
SECRET_KEY=django-insecure-@we$0tpyb&%c8!c$db$v@z&rc9nn)2im*ac$1f(r%hm@(b_1s9
ALLOWED_HOST=locahost:8000,localhost:8080

DB_USER={user} 
DB_PASSWORD={password}
DB_DATABASE={database}

'''