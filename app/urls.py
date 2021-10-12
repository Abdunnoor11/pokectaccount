from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [    
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),    

    path('loan/', views.loan, name='loan'),    
    path('newdebtor/', views.newdebtor, name='newdebtor'),    
    path('debtor/', views.debtor, name='debtor'),
    path('debtorprofile/<int:id>', views.debtorprofile, name='debtorprofile'),

    path('accounts/<int:id>/<str:string>', views.accounts, name='accounts'),    
]
