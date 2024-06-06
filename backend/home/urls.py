from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("authenticate_reg/", views.authenticate_reg, name="authenticate_reg"),
    path("login/", views.login, name="login"),
    path("authenticate_login/", views.authenticate_login, name="authenticate_login"),

    path("password_main/", views.password_main, name="password_main"),
    path("password_add_new/", views.password_add_new, name="password_add_new"),
    path("password_lookup/", views.password_lookup, name="password_lookup"),
]
