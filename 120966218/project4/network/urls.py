
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.create, name="post"),
    path("posts/all", views.getAllPosts, name="all"),
    path("posts/following", views.getFollowedPosts, name="following"),
    path("profile/<int:id>", views.getProfile, name="profile"),
    path("follow/<int:id>", views.Follow, name="follow"),
    path("unfollow/<int:id>", views.Unfollow, name="unfollow"),

    #API paths
    path("like/<int:id>/<str:type>", views.Like, name="like"),
    path("unlike/<int:id>/<str:type>", views.Unlike, name="unlike"),
    path("edit/<int:id>", views.Edit, name="edit"),
    path("save/<int:id>", views.Save, name="save")
]

