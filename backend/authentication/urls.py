from django.urls import path
from .views import *
urlpatterns = [
    path('login/',signin),
    path('signup/',signup),
    path('signout/',signout),
]