from reactpy import component, html
from reactpy_django.router import django_router
from reactpy_router import route


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


    return django_router(
        route("/router/", html.div("Example 1")),
        route("/router/any/<value>/", html.div("Example 2")),
        route("/router/integer/<int:value>/", html.div("Example 3")),
        route("/router/path/<path:value>/", html.div("Example 4")),
        route("/router/slug/<slug:value>/", html.div("Example 5")),
        route("/router/string/<str:value>/", html.div("Example 6")),
        route("/router/uuid/<uuid:value>/", html.div("Example 7")),
        route("/router/two_values/<int:value>/<str:value2>/", html.div("Example 8")),
        route("/router/*", html.div("Fallback")),
    )

