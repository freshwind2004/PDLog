# PDlog
Python3 Django 2 Blog Script

## Requirement

Python > 3.5

Django > 2.2

## Install

### step1: requierd python modules
```
pip3 install Django==2.2.10
pip3 install easy_thumbnails==2.7
```

### step2: test run
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py createsuperuser
```
*here you can create your management account, or skip it,*

*go to domian.com/register and create a normal account*

```
python3 manage.py runserver
```
*test if python modules are all set: no error means all good,*

*otherwise check your python environment. ctrl + c to terminate.*

### step3: run gunicorn
```
pip3 install gunicorn
cd /path/to/the/root/of/this/script
/usr/local/bin/gunicorn -w 2 -b 127.0.0.1:8000 blog.wsgi &
```

### step4: config caddy/nginx

install caddy/nginx the way you like

config Caddyfile:
```
domain.com {
    gzip
    #index index.html
    root /home/domain.com
    proxy / 127.0.0.1:8000 {
        transparent
        except /static /media
    }
    tls off
}
```

config nginx.conf

```
server
    {
        listen 80;
        server_name task.wisemoni.com ;
        index index.html;
        root  /home/domain.com;
        
        ....

        location /media  {
            alias /home/domain.com/media;
            expires      30d;
        }

        location /static {
            alias /home/domain.com/static;
            expires      1d;
        }

        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:8000;
        }
    }
```

### step5: change owner of your script folder 
```
chown -R www:www /home/domain.com
```
otherwise you may not successfully create sql database file, or upload images. note your web user may NOT be 'www', change it as you need.

### step6: turn off debug

edit ./blog/settings.py

change
```
DEBUG = True
```
to
```
DEBUG = False
```
Now enjoy your new blog!
