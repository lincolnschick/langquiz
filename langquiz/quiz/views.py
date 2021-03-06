from django.shortcuts import render
from .languagedata import language_samples
from random import randrange
from .models import Leaderboard
import datetime

def index(request):
    return render(request, "quiz/index.html")

def quiz(request):
    if request.method == "GET":
        context = grab_language_data(request)
        return render(request, "quiz/quiz.html", context)
    else:
        request.session["selection"] = request.POST.get("selection")
        context = {
        "language": request.session["language"],
        "choices": request.session["choices"],
        "selection": request.session["selection"],
        "streak": request.session["streak"],
        "question": request.session["question"]
        }
        if request.session["selection"] != request.session["language"][0]:
            update_database(request)
        
        
    return render(request, "quiz/quiz_answer.html", context)

def leaderboard(request):
    data = Leaderboard.objects.all().order_by("-score")
    context = {
        "leaderboard": data,
        "numbers": [num for num in range(1, data.count() + 1)]
    }
    return render(request, "quiz/leaderboard.html", context)

def grab_language_data(request):
    request.session.clear_expired()

    # Save if previous guess was correct
    increment = False
    if "selection" in request.session and request.session["selection"] == request.session["language"][0]:
        increment = True
    
    context = {}
    # Select random language
    lang = randrange(len(language_samples))

    # Select random text in language
    text = randrange(1, 4)
    context["language"] = [language_samples[lang][0], language_samples[lang][text]]

    # Randomly select additional choices 
    context["choices"] = []
    while len(context["choices"]) < 3:
        choice = randrange(len(language_samples))
        if choice != lang and language_samples[choice][0] not in context["choices"]:
            context["choices"].append(language_samples[choice][0])
    
    request.session["language"] = context["language"]
    
    # Randomly insert correct answer
    random = randrange(4)
    context["choices"].insert(random, language_samples[lang][0])
    request.session["choices"] = context["choices"]
    if increment:
        request.session["question"] += 1
        context["question"] = request.session["question"]
        request.session["streak"] += 1
        context["streak"] = request.session["streak"]
    else:
        request.session["streak"] = context["streak"] = 0
        request.session["question"] = context["question"] = 1
    return context


def update_database(request):
    curr_score = request.session["streak"]
    add_new = False
    if Leaderboard.objects.all().count() < 10:
        add_new = True
    else:
        lowest_score_obj = Leaderboard.objects.order_by("score").first()
        if curr_score > lowest_score_obj.score:
            lowest_score_obj.delete()
            add_new = True
    if add_new:
        username = "Anonymous" if not request.user.is_authenticated else f"{request.user.username}"
        l = Leaderboard(username=username, score=curr_score, date=datetime.date.today())
        l.save()
