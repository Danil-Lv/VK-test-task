from django.contrib import admin
from django.urls import path, include

from friends.yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/v1.0/', include('friends.urls')),
    path('auth/', include('djoser.urls')),
]

urlpatterns += doc_urls
