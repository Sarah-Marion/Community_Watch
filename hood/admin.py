from django.contrib import admin
from .models import Hood, Profile, Business, Post, Join, Social_Amenities

# Register your models here.
admin.site.register(Hood)
admin.site.register(Profile)
admin.site.register(Business)
admin.site.register(Post)
admin.site.register(Join)
admin.site.register(Social_Amenities)