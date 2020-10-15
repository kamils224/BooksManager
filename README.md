# BooksManager
After clone or download: create python virtual env and install required packages:
```sh
$ pip install -r requirements.txt
```
In terminal export your secret key as env variable:
```sh
$ export BOOK_MANAGER_SECRET_KEY="secret key"
```

Production mode:
```sh
$ export DJANGO_DEBUG=False
```
Collect static files before starting the server.
```sh
$ python manage.py collectstatic
```


