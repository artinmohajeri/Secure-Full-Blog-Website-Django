from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomePage.as_view(), name="home_page"),
    path("signup/", views.signup_page, name="signup_page"),
    path("signin/", views.signin_page, name="signin_page"),
    path("blog/<str:username>/<int:id>/", views.blog_page, name="blog_page"),
    path("blogs/", views.blogs_page, name="blogs_page"),
    path("blogs/followings/", views.followings_blogs_page, name="followings_blogs_page"),
    path("users/", views.users, name="users_page"),
    path("profile/<str:username>/", views.profile_page, name="profile_page"),
    path("contact/", views.ContactPage.as_view(), name="contact_page"),
    path("logout/", views.logout_func, name="logout"),
    path("delete_bio/", views.delete_bio, name="delete_bio"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("follow/<str:username>/",views.follow,name="follow"),
    path("unfollow/<str:username>/",views.unfollow,name="unfollow"),
    path("like/<int:id>/",views.like, name="like"),
    path("dislike/<int:id>/",views.dislike, name="dislike"),
]
