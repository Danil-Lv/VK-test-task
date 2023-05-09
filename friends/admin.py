from django.contrib import admin

from .models import User, Application

admin.site.register(User)
admin.site.register(Application)
