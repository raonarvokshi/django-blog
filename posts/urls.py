from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("post/<str:pk>/", views.post, name="post"),
  path("create-blog/", views.create_blog, name="create_blog"),
  path("login/", views.login, name="login"),
  path("register/", views.register, name="register"),
  path("logout/", views.logout, name="logout"),
]