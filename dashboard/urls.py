from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("waiting/", views.waiting, name="waiting"),


    #API
    path("games", views.load_game_list, name="games"),
    path("gamer", views.load_gamer_list, name="gamer"),
    path("profile_update/<int:item>", views.profile_update, name="profile_update"),
    path("find_opp", views.find_opp, name="find_opp"),
    path("find_game", views.find_game, name="find_game"),
    path("match_create", views.match_create, name="match_create"),
]

