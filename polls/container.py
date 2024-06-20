from typing import Any
from django.urls import reverse
from reactpy import component, html
from reactpy.core.types import VdomDictConstructor
from reactpy_django.router import django_router
from reactpy_router import Route, route

from .pages.index_page import index
from .pages.detail_page import detail
from .pages.results_page import results

from utils.types import Props


@component
def vote():
    return html.div("vote")

@component
def navbar():
    return html.nav({'class_name': 'navbar navbar-dark bg-primary mb-4'},
        html.div({'class_name': 'container'},
            html.a({'class_name': 'navbar-brand', 'href': '/'}, "Pollster")
        )
    )

@component
def PageNotFound(msg: str):
    return html.article(
        html.header(
            html.h1("404 Not Found")
        ),
        html.p("Sorry, the page you're looking for doesn't exist."),
        html.a({'href': '/', 'role': 'button', 'class_name': 'outline'}, "Go to Home Page")
    )

@component
def PageContainer(page: VdomDictConstructor, **props: Props):
    return html._(
        navbar(),
        html.div({'class_name': 'container'},
            html.div({'class_name': 'row'},
                html.div({'class_name': '.col-md-6 m-auto'},
                    page(**props)
                )
            )
        )
    )


def page_route(path: str, page: Any) -> Route:
    element = PageContainer(page)
    return route(path, element)

@component
def router():

    root = reverse(f'{__package__}:baseurl', args=[''])[:-1]

    return django_router(
        page_route(f"{root}/", index),
        page_route(f"{root}/<int:pk>/", detail),
        page_route(f"{root}/<int:pk>/results/", results),
        page_route(f"{root}/<int:question_id>/vote/", vote),
    )
