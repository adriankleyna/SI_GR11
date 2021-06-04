from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('work', views.index1, name='index1'),
]