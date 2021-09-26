from django.urls import path
from .views import dashboard, weather, test, plants
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('weather', weather),
    path('upload', test),
    path('plants', plants)
]
