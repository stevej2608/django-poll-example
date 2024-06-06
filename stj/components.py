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

    # https://reactive-python.github.io/reactpy-django/latest/reference/router/
    # https://docs.djangoproject.com/en/5.0/topics/http/urls/#path-converters

    # Routes
    # Example 1 : http://localhost:8000/router/
    # Example 2 : http://localhost:8000/router/any/123/
    # Example 3 : http://localhost:8000/router/integer/123/
    # Example 4 : http://localhost:8000/router/path/123/
    # Example 5 : http://localhost:8000/router/slug/xxx/
    # Example 6 : http://localhost:8000/router/string/xxx/
    # Example 7 : http://localhost:8000/router/uuid/075194d3-6885-417e-a8a8-6c931e272f00/
    # Example 8 : http://localhost:8000/router/two_values/1/test/
    # Example 9 : http://localhost:8000/router/abc/
    # Example 10: http://localhost:8000/router/star/one/
    # Example 11: http://localhost:8000/router/star/weapons?offset=0&limit=10


    return django_router(
        route("/router/", display_params("Example 1")),
        route("/router/any/<value>/", display_params("Example 2")),
        route("/router/integer/<int:value>/", display_params("Example 3")),
        route("/router/path/<path:value>/", display_params("Example 4")),
        route("/router/slug/<slug:value>/", display_params("Example 5")),
        route("/router/string/<str:value>/", display_params("Example 6")),
        route("/router/uuid/<uuid:value>/", display_params("Example 7")),
        route("/router/two_values/<int:value>/<str:value2>/", display_params("Example 8")),

        route("/router/", None, route("abc/", display_params("Example 9"))),

        route("/router/star/", None,
            route("one/", display_params("Example 10")),
            route("*", display_params("Example 11")),
        ),



        route("/router/*", display_params("Fallback")),
    )

