from typing import Any
from django.urls import reverse
from reactpy import component
from reactpy_django.router import django_router
from reactpy_router import Route, route


from .pages import page_container, index, detail, results, Page_404


@component
def spa_router():

    def page_route(path: str, page: Any) -> Route:
        element = page_container(page)
        return route(path, element)

    root = reverse('polls:index')[:-1]

    return django_router(
        page_route(f"{root}/<int:pk>/", detail),
        page_route(f"{root}/<int:pk>/results/", results),
        page_route(f"{root}/", index),
        page_route("/", index),
        page_route("*", Page_404)
    )
