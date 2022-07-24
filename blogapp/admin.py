from django.contrib import admin
from blogapp.models import Blog,Comments,UserProfile
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Blog)
admin.site.register(Comments)

