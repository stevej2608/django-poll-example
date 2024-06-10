from django.urls import reverse
from reactpy import component, html
from reactpy_django.router import django_router
from reactpy_router import route

from .pages.index_page import index
from .pages.detail_page import detail
from .pages.results_page import results


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
def router():

    root = reverse(f'{__package__}:baseurl', args=[''])[:-1]

    return django_router(
        route(f"{root}/", index()),
        route(f"{root}/<int:pk>/", detail()),
        route(f"{root}/<int:pk>/results/", results()),
        route(f"{root}/<int:question_id>/vote/", vote()),
    )
