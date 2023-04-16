from django.urls import path
from user.views import login, signup, logout

app_name = "user"
urlpatterns = [
    path("user/login/", login, name="login"),
    path("user/signup/", signup, name="signup"),
    path("user/logout", logout, name="logout"),
]
