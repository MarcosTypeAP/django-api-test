"""Users URLs"""

# Django
from django.urls import path

# Views
from users.views import UserLoginView, UserSignUpView


urlpatterns = [

    path("login/", UserLoginView.as_view(), name="login"),

    path("signup/", UserSignUpView.as_view(), name="signup"),

]