from django.contrib import admin
from django.urls import path
from resume.views import index, generate


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('submit/', generate, name='generate')
]
