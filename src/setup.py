NGINX_PORT = 8080
PROJECT_DIR = "c:/software/prison/"
NGINX_CONF = '''
server{
    listen 8080;
    server_name localhost;

    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options nosniff;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias c:/projects/app1/staticfiles/;
        autoindex off;
    }
    
    location /media/ {
        alias c:/projects/app1/media/;
        autoindex off;
    }
}
'''