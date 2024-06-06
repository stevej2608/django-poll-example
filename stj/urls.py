from django.urls import re_path
from .views import router
urlpatterns = [
    re_path(r"^router/(?P<path>.*)/?$", router),
]
