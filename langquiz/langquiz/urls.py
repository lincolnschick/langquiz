from django.urls import path, include
from users import views as v

urlpatterns = [
    path("", include("quiz.urls")),
    path("", include("django.contrib.auth.urls")),
    path("register/", include("users.urls")),
]
