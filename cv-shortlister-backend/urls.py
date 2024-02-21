from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from resume.views import index, generate, poll


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('submit/', generate, name='generate'),
    path('poll/', poll, name='polling'),
    path('<path:dummy>/', RedirectView.as_view(url='https://parse.cvninja.studio/', permanent=False)),
]