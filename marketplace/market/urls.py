from django.urls import path
from .views import RegisterUserView, HomePageView, LoginUserView

urlpatterns = [
    path("home/", HomePageView.as_view(), name="home"),
    path("register_user/", RegisterUserView.as_view(), name="register_user"),
    path("login_user/", LoginUserView.as_view(), name="login_user"),
]
