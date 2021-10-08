from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [    
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),    

    path('loan/', views.loan, name='loan'),    
    path('credit/', views.credit, name='credit'),
    path('deposit/', views.deposit, name='deposit'),
]
