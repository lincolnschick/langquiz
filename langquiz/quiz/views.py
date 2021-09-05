from django.shortcuts import render
from .languagedata import language_samples
from random import randrange


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
    return render(request, "quiz/quiz_answer.html", context)


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
