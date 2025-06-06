# Dev 

## Run Docker Locally

Add to /etc/hosts

```
127.0.0.1    test.staticpatch
127.0.0.1    1.test.staticpatch
127.0.0.1    2.test.staticpatch
127.0.0.1    3.test.staticpatch
127.0.0.1    4.test.staticpatch
127.0.0.1    5.test.staticpatch
127.0.0.1    6.test.staticpatch
127.0.0.1    7.test.staticpatch
127.0.0.1    8.test.staticpatch
127.0.0.1    9.test.staticpatch
```

To setup (run from root directory of repostiory, not the `dev` directory):

```
docker build --tag staticpatchdevubuntu2404 -f dev/dev.ubuntu.2404.Dockerfile .
docker run -d --name staticpatchdevubuntu2404 -p 80:80 -p 443:443  -p 8888:8888 -v .:/home/staticpatch/code staticpatchdevubuntu2404
```

If already setup, start:

```
docker start staticpatchdevubuntu2404
```

To connect into the container as root user (sometimes needed):

```
docker exec -it -u 0 staticpatchdevubuntu2404 /bin/bash
```

To connect into the container as normal user:

```
docker exec -it -u 2000 staticpatchdevubuntu2404 /bin/bash
```

To stop:

```
docker stop staticpatchdevubuntu2404
```

## Dev Container

You can also use a dev container.

Normally you will be connected as the staticpatch user, but you can run `sudo /bin/bash` to become root.

With this option you can view the admin site, but there may be issues viewing the static sites.

## To use

The domains listed above all have self-signed SSL certificates set up, so you can use them and test the response.

To setup, open one connection to the container as normal user (or open a terminal if in dev containers) and run:

```
cd staticpatch/
STATICPATCH_FILE_STORAGE=/home/staticpatch/storage python3 manage.py migrate
STATICPATCH_FILE_STORAGE=/home/staticpatch/storage python3 manage.py setupstorage
STATICPATCH_FILE_STORAGE=/home/staticpatch/storage python3 manage.py createsuperuser
```

To run after setup, as normal user open a connection / open a terminal and run:

```
sudo apachectl start
cd staticpatch/
STATICPATCH_FILE_STORAGE=/home/staticpatch/storage python3 manage.py runserver 0.0.0.0:8888
```

Then as normal user open another connection / open another terminal and run:

```
cd staticpatch/
STATICPATCH_FILE_STORAGE=/home/staticpatch/storage python3 manage.py db_worker
```

To send a site to this:
```
curl -X POST "http://localhost:8888/api/site/SITE/publish_built_site"  -H  "Content-Type: multipart/form-data" -H "Security-Key: your_security_key_here" -F "built_site=@\"dev/test_site.zip\""
curl -X POST "http://localhost:8888/api/site/SITE/preview/PREVIEW/instance/INSTANCE/publish_built_site"  -H  "Content-Type: multipart/form-data" -H "Security-Key: your_security_key_here" -F "built_site=@\"dev/test_site.zip\""
curl -X POST "http://localhost:8888/api/site/SITE/preview/PREVIEW/instance/INSTANCE/deactivate"  -H "Security-Key: your_security_key_here"
```
