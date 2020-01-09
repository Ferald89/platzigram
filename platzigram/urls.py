"""Platzigram URLs module."""

# Django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    #path adming
    path('admin/', admin.site.urls),
    #path posts
    path('',include(('posts.urls','posts'),namespace='posts')),

    #path users
    path('users/',include(('users.urls','users'),namespace='users')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
