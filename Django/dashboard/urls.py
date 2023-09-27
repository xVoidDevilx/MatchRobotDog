from django.urls import path
from . import views

#urlConfiguration module
urlpatterns = [
    path('hello/', views.captureKeyEvent)
]