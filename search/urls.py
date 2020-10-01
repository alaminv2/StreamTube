from django.urls import path
from . import views

app_name = 'search_app'

urlpatterns = [
    path('', views.searchView, name="search"),
    path('play/<str>/', views.playViedeo, name="play"),
]
