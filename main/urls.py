from django.urls import path
from main import views
from django.db import connection

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.login,name='login')
]

