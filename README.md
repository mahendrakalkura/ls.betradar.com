How to install?
===============

```
$ git clone --recursive git@github.com:mahendrakalkura/ls.betradar.com.git
$ cd ls.betradar.com
$ mkvirtualenv --python=python3 ls.betradar.com
$ pip install --requirement requirements.txt
```

How to run?
===========

```
$ cd ls.betradar.com
$ workon ls.betradar.com
$ python manage.py --download
$ python manage.py --report --event-full-feed --statuses
$ python manage.py --report --match-timeline --types
$ python manage.py --report --match-timeline --ballcoordinates
$ python manage.py --report --match-timeline --events $id
```
