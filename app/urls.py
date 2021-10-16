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

    path('invest/', views.invest, name='invest'),    
    path('newlender/', views.newlender, name='newlender'),    
    path('lender/', views.lender, name='lender'),
    path('lenderprofile/<int:id>', views.lenderprofile, name='lenderprofile'),

    path('land/', views.land, name='land'),
    path('newlandowner/', views.newlandowner, name='newlandowner'),

    path('accounts/<int:id>/<str:string>', views.accounts, name='accounts'),    
    path('lenderaccounts/<int:id>/<str:string>', views.lenderaccounts, name='lenderaccounts'),    
]
