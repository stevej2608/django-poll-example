from django.urls import path, re_path
from .views import router

app_name = __package__

urlpatterns = [
    path('', router, name='index'),
    path('<int:pk>/', router, name='detail'),
    path('<int:pk>/results/', router, name='results'),
    path('<int:question_id>/vote/', router, name='vote'),
    re_path(r"(?P<path>.*)/?$", router, name="baseurl"),
]
