from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),



    #API
    path("load_match", views.load_match, name="load_match"),
    path("update_match/<int:id>", views.update_match, name="update_match"),
    path("turn_change/<int:id>", views.turn_change, name="turn_change"),
]