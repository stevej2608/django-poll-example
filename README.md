# django-basic

![](./docs/img/Screenshot.png)

Steps used in the tutorial [Writing your first Django app]

        django-admin startproject project

        cd project
        python manage.py runserver

        python manage.py startapp polls

        python manage.py runserver localhost:8000

Visit [http://localhost:8000/polls/](http://localhost:8000/polls/)

        python manage.py migrate

        python manage.py makemigrations polls
        python manage.py sqlmigrate polls 0001
        python manage.py migrate

        python manage.py createsuperuser

Code up the project [django-polls], and then run the finished project:

        python manage.py runserver localhost:8000

Visit [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Testing 

        python manage.py test polls

## Improvements

### Admin dashboard

Added [django-unfold]

### Added bootstrap based templates

Changed view templates for the ones in [Voting System Project Using Django Framework]

![](https://media.geeksforgeeks.org/wp-content/uploads/20200514105612/pollster-web-app.png)


* [django-unfold], Modern Django admin theme for seamless interface development
* [Writing your first Django app]
* [django-polls]


[Voting System Project Using Django Framework]: https://www.geeksforgeeks.org/voting-system-project-using-django-framework/
[django-unfold]: https://github.com/unfoldadmin/django-unfold
[Writing your first Django app]: https://docs.djangoproject.com/en/5.0/intro/tutorial01/
[django-polls]: https://github.com/do-community/django-polls