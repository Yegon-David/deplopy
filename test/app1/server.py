from waitress import serve
from app1.wsgi import application

if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=8000)