from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path("register/", views.register_user),
    path("login/", views.login_user),
    path("logout/", views.logout_user),
    path("<int:user_id>/", views.view_user),
]