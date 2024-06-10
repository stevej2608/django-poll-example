from django.urls import re_path
from .views import router

app_name = __package__

urlpatterns = [
    re_path(r"(?P<path>.*)/?$", router, name="baseurl"),
]
