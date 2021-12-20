from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from dashboard.models import Match
import json

# Create your views here.

@login_required(login_url='')
def index(request):
    return render(request, "game/index.html",{
        'user': request.user.username,
    })

@login_required(login_url='')
def load_match(request):
    match = Match.objects.get(id = request.GET.get('id'))
    if match.opp1 == request.user:
        u = 1
    if match.opp2 == request.user:
        u = 2
    return JsonResponse({
        "match" : match.serialize(),
        "user": u}
        , safe=False)


@login_required(login_url='')
def update_match(request, id):
    try:
        match = Match.objects.get(id = id)
    except Match.DoesNotExist:
        return JsonResponse({"error": "Match not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)

        if data.get("b1_sel") is not None:
            match.opp1_ball_sel = data["b1_sel"]
        if data.get("b2_sel") is not None:
            match.opp2_ball_sel = data["b2_sel"]
        if data.get("b1_guess") is not None:
            match.opp1_ball_guess = data["b1_guess"]
        if data.get("b2_guess") is not None:
            match.opp2_ball_guess = data["b2_guess"]
        match.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
    

@login_required(login_url='')
def turn_change(request, id):
    try:
        match = Match.objects.get(id = id)
    except Match.DoesNotExist:
        return JsonResponse({"error": "Match not found."}, status=404)

    turn = match.turn

    if turn == 0:
        r = bool(match.opp2_ball_sel % 2)
             
        if match.opp1_ball_guess == r:
            match.opp2_ball -= match.opp2_ball_sel
            match.opp1_ball += match.opp2_ball_sel
        else:
            match.opp2_ball += match.opp2_ball_sel
            match.opp1_ball -= match.opp2_ball_sel
        
        match.opp2_ball_sel = 0
    elif turn == 1:
        r = bool(match.opp1_ball_sel % 2)  
            
        if match.opp2_ball_guess == r:
            match.opp2_ball += match.opp1_ball_sel
            match.opp1_ball -= match.opp1_ball_sel
        else:
            match.opp2_ball -= match.opp1_ball_sel
            match.opp1_ball += match.opp1_ball_sel
        
        match.opp1_ball_sel = 0
    else:
        pass
    
    if match.opp1_ball <= 0:
        match.opp1_ball = 0
        turn = 2
        match.winner = match.opp2
        match.active = False
    elif match.opp2_ball <= 0:
        match.opp2_ball = 0
        turn = 2
        match.winner = match.opp1
        match.active = False
    else:
        if turn == 1:
            turn = 0
        else:
            turn = 1

    match.turn = turn
    match.save()    
    
    return JsonResponse({
        "done": match.opp1_ball_guess,
        })

      
    
        


