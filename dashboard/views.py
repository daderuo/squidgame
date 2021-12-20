from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db import IntegrityError
from django.http import JsonResponse
from django.core import serializers
import json
from django.db.models import Q

# Create your views here.

@login_required()
def index(request):
    return render(request, "dashboard/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "dashboard/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = username + '@dadegames.com'
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "dashboard/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "dashboard/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "dashboard/register.html")

@login_required
def load_game_list(request):
    games = Game.objects.all()       
    games = games.order_by("id").all()
    return JsonResponse([game.serialize() for game in games], safe=False)

@login_required
def load_gamer_list(request):
    gamers = User.objects.all()

    for gamer in gamers:
        t = Match.objects.filter(Q(opp1 = gamer) | Q(opp2 = gamer), active = False).count()
        w = Match.objects.filter(winner = gamer, active = False).count()
        gamer.total_games = t
        gamer.win_games = w
        gamer.save()

    gamers = gamers.order_by("-win_games").all()
    return JsonResponse([gamer.serialize() for gamer in gamers], safe=False)

@login_required
def profile_update(request,item):
    user = User.objects.get(username = request.user)
    if item == 1:
        user.total_games += 1
    elif item == 2:
        user.win_games += 1
    user.save()
    return JsonResponse({
        "done": True
        })

@login_required
def find_opp(request):
    game_id = request.GET.get('game')
    ops = Wait.objects.all() 
    u = User.objects.get(username = request.user)
    for op in ops:
        if op.opp != u:
            op.delete()
            return JsonResponse({
                "op": True,
                "user": op.opp.username,
            })
    if ops.count() == 0:
        g = Game.objects.get(id = game_id)
        w = Wait(opp = u, game = g)
        w.save()
    return JsonResponse({
            "op": False,
            })

@login_required
def waiting(request):
    return render(request, "dashboard/waiting.html")


@login_required
def find_game(request):
    g = Game.objects.get(id = request.GET.get('game'))
    u = User.objects.get(username = request.user)
    try:
        match = Match.objects.get(Q(opp1 = u) | Q(opp2 = u), active = True, game = g)
    except Match.DoesNotExist:
        return JsonResponse({
            "match": False,
            })
  
    return JsonResponse({
    "match": True,
    "id": match.id,
    })
        

    


@login_required
def match_create(request):
    g = Game.objects.get(id=request.GET.get('game'))
    opp = request.GET.get('opp')
    u1 = User.objects.get(username = opp)
    u2 = User.objects.get(username = request.user)
    m = Match(opp1 = u1, opp2 = u2, game = g, winner = u1)
    m.save()
    return JsonResponse({
        "done": True,
        "match_id": m.id
        })