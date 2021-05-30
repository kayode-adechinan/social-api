from django.urls import path, include
from user import views

app_name = "account"
urlpatterns = [
    path("users/me/", views.UpdateProfilAPI.as_view()),
    path("auth/sign-up/", views.SignUpAPI.as_view()),
    path("auth/sign-in/", views.SignInAPI.as_view()),
    path("auth/reset-password/", views.ResetPasswordAPI.as_view()),
    path("auth/change-password/", views.ChangePasswordAPI.as_view()),
]
