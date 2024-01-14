from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, User
from django.contrib.auth.hashers import make_password
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, null=False, blank=False, default="")
    password = models.CharField(max_length=128,  null=False, blank=False, default="")
    fname = models.CharField(max_length=30, null=False, blank=False)
    lname = models.CharField(max_length=30, null=False, blank=False)
    bio = models.TextField(blank=True, null=True)
    pic = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default="profile_pictures/default-profile.jpg")
    followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='user_followers')
    followings = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='user_followings')

    def total_followers(self):
        return self.followers.count()
    
    def total_followings(self):
        return self.followings.count()

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fname', 'lname']

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if not self.id:  # If the user is being created (not updated)
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Blog(models.Model):
    pic = models.ImageField(upload_to='blog_pictures/', blank=True, null=True, default="blog_pictures/img-1.jpg")
    title = models.CharField(max_length=50, null=False, blank=False, default="")
    body = models.TextField(null=False, blank=False, default="")
    likes = models.ManyToManyField(CustomUser, blank=True, symmetrical=False, related_name='blog_likes')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blogs')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return str(f"{self.title}   |   {self.body[:50]}")