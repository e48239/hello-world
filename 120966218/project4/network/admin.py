from django.contrib import admin
from .models import User, Post, Profile

# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Profile)
