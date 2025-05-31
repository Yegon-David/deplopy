WAITRESS = '''
<service>
  <id>{project}</id>
  <name>{project} service</name>
  <description>This will start Django service using waitress.</description>

  <executable>{path}\\.venv\\Scripts\\python.exe</executable>
  <arguments>
    <argument>-m</argument>
    <argument>waitress</argument>
    <argument>--listen=0.0.0.0:8000</argument>
    <argument>{project}.wsgi:application</argument>
  </arguments>
  <workingdirectory>{path}</workingdirectory>

  <logpath>{path}\\logs</logpath>
  <log mode="roll-by-size">
  <sizeThreshold>10240</sizeThreshold>
  <keepFiles>5</keepFiles>
  </log>
  
  <onfailure action="restart" delay="5 sec" />

</service>
'''
NGINX_SERVICE = '''
<service>
  <id>nginx</id>
  <name>Nginx Server</name>
  <description>This runs nginx webserver to server waitress</description>

 <workingdirectory>{path}</workingdirectory> 
  <executable>{exe_file}</executable>
  <logpath>{base_dir}\logs</logpath>
  <log mode="roll-by-size">
    <sizeThreshold>10240</sizeThreshold>
    <keepFiles>5</keepFiles>
  </log>
  
  <onfailure action="restart" delay="5 sec" />

</service>
'''
NGINX_BASE_CONFIG = '''
worker_processes  1;
events {{
    worker_connections  1024;
}}
http {{
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    #gzip  on;
    server {{
        listen       80;
        server_name  localhost;
        location / {{
            root   html;
            index  index.html index.htm;
        }}
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {{
            root   html;
        }}
    }}
    include {custom_config_path};
}}
'''
NGINX_APP_CONF = '''
server{{
    listen 8080;
    server_name localhost;

    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options nosniff;

    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}

    location /static/ {{
        alias {base_dir}/staticfiles/;
        autoindex off;
    }}
    
    location /media/ {{
        alias {base_dir}/media/;
        autoindex off;
    }}
}}
'''
