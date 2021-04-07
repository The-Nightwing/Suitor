from django.urls import path
from main import views
from django.db import connection

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.login,name='login'),
    path('loginrequest',views.loginaccess,name='loginrequest'),
    path('para_query1',views.paralegal, name='para_query1'),
    path('para_query2',views.paralegal, name='para_query2'),
    path('para_query3',views.paralegal, name='para_query3'),
    path('para_query4',views.paralegal, name='para_query4'),
    path('customer_1',views.customer,name='customer_query1'),
    path('customer_2',views.customer,name='customer_query2'),
    path('customer_3',views.customer,name='customer_query3'),
    path('customer_4',views.customer,name='customer_query4')
]

