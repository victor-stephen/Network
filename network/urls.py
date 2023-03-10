
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API Routes
    path("addPost", views.addPost, name="addPost"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("follow/<int:profile_id>", views.follow, name="follow"),
    path("unfollow/<int:profile_id>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("editPost/<int:post_id>", views.editpost, name="editPost"),

]
