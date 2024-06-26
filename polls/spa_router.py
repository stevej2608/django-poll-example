from typing import Any
from django.urls import reverse
from reactpy import component
from reactpy_django.router import django_router
from reactpy_router import Route, route
from reactpy_django.hooks import use_user

from .pages import page_container, index, detail, results, Page_404, Page_401

# https://reactive-python.github.io/reactpy-django/latest/reference/decorators/?h=user#user-passes-test
# https://reactive-python.github.io/reactpy-django/latest/reference/router/

@component
def spa_router():

    def page_route(path: str, page: Any, authenticate_user = False) -> Route:

        user = use_user()

        if authenticate_user and not user.is_authenticated:
            element = page_container(Page_401)
        else:
            element = page_container(page)

        return route(path, element)

    root = reverse('polls:index')[:-1]

    return django_router(
        page_route(f"{root}/<int:pk>/", detail),
        page_route(f"{root}/<int:pk>/results/", results, authenticate_user=True),
        page_route(f"{root}/", index),
        page_route("/", index),
        page_route("*", Page_404)
    )
