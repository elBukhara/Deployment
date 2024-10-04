# Deployment of a Test Project

Демонтрация процесса деплоймента на виртуальную машину Google Cloud - [link](https://www.youtube.com/watch?v=dKnYNrBoqQc)

## Quickstart

Run the following commands to bootstrap your environment:
    
    sudo apt-get update
    sudo apt-get install -y git python3-dev python3-venv python3-pip supervisor nginx vim mysql-server libmysqlclient-dev
    git clone https://github.com/your-profile/your-project-name
    cd your-project-name/
  
    python3 -m venv .venv   
    source .venv/bin/activate
    pip3 install -r requirements/prod.txt 

## .ENV files

    cd app
    vim .env
    i // to enter insert mode
    // paste the data
    ESC // to exit insert mode
    :wq // to save and quit in one step
    
    while read file; do
        export "$file"
        done < .env

    printenv | grep SECRET

## MySQL inside VM:

[StackOverflaw](https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost)

(replace YOUR_SYSTEM_USER with the username you have)

    SELECT User, Host, plugin FROM mysql.user;
    sudo mysql -u root # I had to use "sudo" since it was a new installation
    SELECT User, Host, plugin FROM mysql.user;

    mysql> USE mysql;
    mysql> CREATE USER 'YOUR_SYSTEM_USER'@'localhost' IDENTIFIED BY 'YOUR_PASSWD';
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'YOUR_SYSTEM_USER'@'localhost';
    mysql> UPDATE user SET plugin='auth_socket' WHERE User='YOUR_SYSTEM_USER';
    mysql> FLUSH PRIVILEGES;
    mysql> exit;

    sudo service mysql restart

Remember that if you use option #2 you'll have to connect to MySQL as your system username (mysql -u YOUR_SYSTEM_USER).
Creating a database for a Django Project:

    mysql -u YOUR_SYSTEM_USER -p
    // enter password
    CREATE DATABASE your_database_name;
    GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_username'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;

Migrating (/app):

    python3 manage.py makemigrations --settings=deployment.settings.prod
    python3 manage.py migrate --settings=deployment.settings.prod
    python3 manage.py loaddata data.json --settings=deployment.settings.prod

Run the app with Waitress:

    waitress-serve --listen=127.0.0.1:8000 deployment.wsgi:application
    
Collect static files (/app):

    python3 manage.py collectstatic --settings=deployment.settings.prod

## NGINX   

Routing into NGINX file:

    sudo vim /etc/nginx/sites-enabled/default  
    
Config file (paste the following):

    server {
            listen 80 default_server;
            listen [::]:80 default_server;

            location /static/ {
                alias /home/shakhzod/Deployment/app/static/; 
            }

            location /media/ {
                alias /home/shakhzod/Deployment/app/media/; 
            }

            location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_redirect off;
                add_header P3P 'CP="ALL DSP COR PSAa OUR NOR ONL UNI COM NAV"';
                add_header Access-Control-Allow-Origin *;
        }
    }

Allow access for static and media files to NGINX:

    sudo usermod -a -G shakhzod www-data
    
Restart NGINX:
    
    sudo service nginx restart

Run again with Waitress:

    waitress-serve --listen=127.0.0.1:8000 deployment.wsgi:application

## Supervisor:

    cd /etc/supervisor/conf.d/deployment.conf
    sudo vim deployment.conf
    
Config file:
    
    [program:deployment]
    command=/bin/bash -c 'source /home/shakhzod/Deployment/.venv/bin/activate && cd app && gunicorn deployment.wsgi:application -b 127.0.0.1:8000 -w 4 --timeout 90'
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/deployment.err.log
    stdout_logfile=/var/log/deployment.out.log
    directory=/home/shakhzod/Deployment
    user=shakhzod
    startsecs=0
    environment=PATH="/home/shakhzod/Deployment/.venv/bin",DJANGO_SETTINGS_MODULE="deployment.settings.prod"

    
Update supervisor with the new process:
    
    sudo supervisorctl reread
    sudo supervisorctl update
    
To restart the process after the code updates run:

    sudo supervisorctl restart deployment

Checking ports that are run by Supervisor/Gunicorn, Killing Ports:

    sudo lsof -i :8000
    sudo kill -9 $(sudo lsof -t -i:8000)