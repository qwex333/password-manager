from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("register_page/", views.register_page, name="register_page"),
    path("register_authn/", views.register_authn, name="register_authn"),
    # path("login_page/", views.login_page, name="login_page"),
    path("login_authn/", views.login_authn, name="login_authn"),

    path("password_main/", views.password_main, name="password_main"),
    path("password_add_new/", views.password_add_new, name="password_add_new"),
    path("password_lookup/", views.password_lookup, name="password_lookup"),
]
