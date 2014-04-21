Introduction
------------

Barrow is a configurable web spider

How to use it?
--------------

1. Install packages from requirements.txt
2. python manage.py syncdb && python manage.py migrate
3. python manage.py runserver
4. config your own json spider, add to database through http://localhost:8000/xadmin/

Translation
-----------

If you want to use translation, please run the following command to compile po files first::

    $ python manage.py compilemessages

And change your language code in local_settings.py