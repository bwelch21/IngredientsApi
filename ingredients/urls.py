from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('ingredients/batch', csrf_exempt(views.batch_get_ingredients), name='get_ingredients')
]