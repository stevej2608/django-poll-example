from typing import Any
from django.urls import reverse
from reactpy import component, html
from reactpy.core.types import VdomDictConstructor
from reactpy_django.router import django_router
from reactpy_router import Route, route, link

from utils.types import Props

from .pages.index_page import index
from .pages.detail_page import detail
from .pages.results_page import results
from .pages.page_404 import Page_404


@component
def _navbar():
    return html.nav({'class_name': 'navbar navbar-dark bg-primary mb-4'},
        html.div({'class_name': 'container'},
            link(html.div({'class_name': 'btn navbar-brand'}, "Pollster"), to="/polls/"),
        ),

        html.ul({'class_name': 'navbar-nav ml-auto'},
            html.li({'class_name': 'nav-item'},
                html.a({'class_name': 'btn navbar-brand', 'href': '/admin/'}, "Admin")
            )
        )


    )

@component
def _page_not_found(msg: str):
    return html.article(
        html.header(
            html.h1("404 Not Found")
        ),
        html.p("Sorry, the page you're looking for doesn't exist."),
        html.a({'href': '/', 'role': 'button', 'class_name': 'outline'}, "Go to Home Page")
    )

@component
def _page_container(page: VdomDictConstructor, **props: Props):
    return html._(
        _navbar(),
        html.div({'class_name': 'container'},
            html.div({'class_name': 'row'},
                html.div({'class_name': '.col-md-6 m-auto'},
                    page(**props)
                )
            )
        )
    )


def _page_route(path: str, page: Any) -> Route:
    element = _page_container(page)
    return route(path, element)


@component
def router():

    root = reverse('polls:index')[:-1]

    return django_router(
        _page_route(f"{root}/", index),
        _page_route(f"{root}/", index),
        _page_route(f"{root}/<int:pk>/", detail),
        _page_route(f"{root}/<int:pk>/results/", results),
        _page_route("/", index),
        _page_route("*", Page_404)
    )
