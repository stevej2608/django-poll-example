from django.urls import reverse
from reactpy import component, html, use_location
from reactpy_django.router import django_router
from reactpy_router import route, use_params, use_query


@component
def display_params(string: str):
    location = use_location()
    query = use_query()
    params = use_params()

    return html._(
        html.div({"id": "router-string"}, string),
        html.div(f"Params: {params}"),
        html.div(
            {"id": "router-path", "data-path": location.pathname},
            f"Path Name: {location.pathname}",
        ),
        html.div(f"Query String: {location.search}"),
        html.div(f"Query: {query}"),
    )


@component
def main():

    root = reverse(f'{__package__}:baseurl', args=[''])[:-1]

    # https://reactive-python.github.io/reactpy-django/latest/reference/router/
    # https://docs.djangoproject.com/en/5.0/topics/http/urls/#path-converters

    # Routes
    # Example 1 : http://localhost:8000/stj/
    # Example 2 : http://localhost:8000/stj/any/123/
    # Example 3 : http://localhost:8000/stj/integer/123/
    # Example 4 : http://localhost:8000/stj/path/123/
    # Example 5 : http://localhost:8000/stj/slug/xxx/
    # Example 6 : http://localhost:8000/stj/string/xxx/
    # Example 7 : http://localhost:8000/stj/uuid/075194d3-6885-417e-a8a8-6c931e272f00/
    # Example 8 : http://localhost:8000/stj/two_values/1/test/
    # Example 9 : http://localhost:8000/stj/abc/
    # Example 10: http://localhost:8000/stj/star/one/
    # Example 11: http://localhost:8000/stj/star/weapons?offset=0&limit=10


    return django_router(
        route(f"{root}/", display_params("Example 1")),
        route(f"{root}/any/<value>/", display_params("Example 2")),
        route(f"{root}/integer/<int:value>/", display_params("Example 3")),
        route(f"{root}/path/<path:value>/", display_params("Example 4")),
        route(f"{root}/slug/<slug:value>/", display_params("Example 5")),
        route(f"{root}/string/<str:value>/", display_params("Example 6")),
        route(f"{root}/uuid/<uuid:value>/", display_params("Example 7")),
        route(f"{root}/two_values/<int:value>/<str:value2>/", display_params("Example 8")),

        route(f"{root}/", None, route("abc/", display_params("Example 9"))),

        route(f"{root}/star/", None,
            route("one/", display_params("Example 10")),
            route("*", display_params("Example 11")),
        ),

        route(f"{root}/*", display_params("Fallback")),
    )
