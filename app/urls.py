from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomePage.as_view(), name="home_page"),
    path("signup", views.signup_page, name="signup_page"),
    path("signin", views.signin_page, name="signin_page"),
    path("blog", views.BlogPage.as_view(), name="blog_page"),
    path("blogs", views.BlogsPage.as_view(), name="blogs_page"),
    path("users", views.users, name="users_page"),
    path("profile/<str:username>/", views.profile_page, name="profile_page"),
    path("contact", views.ContactPage.as_view(), name="contact_page"),
    path("logout", views.logout_func, name="logout"),
    path("delete_bio", views.delete_bio, name="delete_bio"),
    path("delete_account", views.delete_account, name="delete_account"),
]
