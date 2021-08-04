from django.shortcuts import render
from .languagedata import language_samples
from random import randrange


def index(request):
    return render(request, "quiz/index.html")

def quiz(request):
    context = grab_language_data()
    return render(request, "quiz/quiz.html", context)

def grab_language_data():
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
        if choice != lang:
            context["choices"].append(language_samples[choice][0])

    # Randomly insert correct answer
    random = randrange(4)
    context["choices"].insert(random, language_samples[lang][0])

    return context
