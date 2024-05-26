# django-basic

        django-admin startproject project

        cd project
        python manage.py runserver

        python manage.py startapp polls

Visit [http://localhost:8000/polls/](http://localhost:8000/polls/)

        python manage.py migrate

        python manage.py makemigrations polls
        python manage.py sqlmigrate polls 0001
        python manage.py migrate

        python manage.py createsuperuser

Visit [http://localhost:8000/admin/](http://localhost:8000/admin/)




* [Writing your first Django app](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
* [django-polls](https://github.com/do-community/django-polls)