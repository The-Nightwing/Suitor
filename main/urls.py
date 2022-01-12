from django.urls import path
from main import views
from django.db import connection

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',views.index, name="index-1"),
    path('services', views.services, name='services'),
    path('contact-us', views.contact_us, name='contact-us'),
    path('about-us', views.about_us, name='about-us'),
    path('login',views.login,name='login'),
    path('loginrequest',views.loginaccess,name='loginrequest'),
    path('paralegal',views.paralegal, name='paralegal'),
    path('customer',views.customer,name='customer'),
    path('form_lawyer',views.user_search_lawyer_query, name='form_lawyer'),
    path('lawyer',views.lawyer,name='lawyer'),
    path('otherstaff',views.otherstaff,name='otherstaff'),
    path('managing_partner',views.managing_partner,name='managing_partner'),
    path('meeting_form',views.meeting_form,name='meeting_form'),
    path('customer_client',views.customer_client,name='customer_client')
]

