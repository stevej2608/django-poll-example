from django.urls import path, re_path
from .views import spa_router

app_name = __package__

urlpatterns = [
    path('', spa_router, name='index'),
    path('<int:pk>/', spa_router, name='detail'),
    path('<int:pk>/results/', spa_router, name='results'),
    re_path(r"(?P<path>.*)/?$", spa_router, name="baseurl"),
]
