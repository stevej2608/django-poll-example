# reactpy-django-polls

![](./docs/img/screenshot.jpg)

An example of using [reactpy-django] to create a simple, Django based, single 
page application (SPA). The project is a reworking of the introductory 
Django project: [Writing your first Django app]. If you are unfamiliar 
with Django get up to speed by working through this first.

## Usage

        git clone https://github.com/stevej2608/reactpy-django-polls

        cd reactpy-django-polls
        poetry install --no-root

        python manage.py runserver localhost:8000

Visit [http://localhost:8000](http://localhost:8000)


Use Django admin to add/remove questions. Visit [Admin](http://localhost:8000/admin/) or
simply click the **Admin** link, top-right in every page, (credentials user:admin, password:admin). 

## Features

- [X] No templates, all pages are coded in python alone.
- [X] Uses 
- [X] Integrates with Django ORM using *use_query* and *use_mutation* hooks.
- [X] Can be used along side other Django apps

## Code Overview

 [reactpy-django] makes no changes to the Django ecosystem. The package provides
 a bridge that maps standard Django routes, as defined by urls, views 
 and templates, onto [reactpy] components. One or many such mapping can be 
 defined. 
 
 As with any Django app [urls.py](./polls/urls.py) defines a URL
 pattern that maps onto a [view](/workspaces/django/basic/polls/views.py). The
 view, in turn, loads a [template](polls/templates/index.html), 
 
 The bridge between Django and [reactpy-django] is defined in the template:

*[index.html](polls/templates/index.html)*
 ```
 {% load reactpy %}

<body>
	{% component "polls.spa_router.spa_router" %}
</body>
 ``` 




## Links

* [reactpy]
* [reactpy-django]: https://reactive-python.github.io/reactpy-django/latest/
        * [use-mutation](https://reactive-python.github.io/reactpy-django/latest/reference/hooks/#use-mutation)
* [django-unfold], Modern Django admin theme for seamless interface development
* [Writing your first Django app]
* [django-polls]
* [Bootstrap Pulse Theme]


[reactpy]: https://reactpy.dev/docs/index.html
[Bootstrap Pulse Theme]: https://bootswatch.com/4/pulse/
[Voting System Project Using Django Framework]: https://www.geeksforgeeks.org/voting-system-project-using-django-framework/
[django-unfold]: https://github.com/unfoldadmin/django-unfold
[Writing your first Django app]: https://docs.djangoproject.com/en/5.0/intro/tutorial01/
[django-polls]: https://github.com/do-community/django-polls