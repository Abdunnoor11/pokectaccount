from django.db import models
from django.contrib.auth.models import User
import os


class Debtor(models.Model):
    debtorName = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null= True)
    address = models.TextField(blank=True, null= True)
    img = models.ImageField(upload_to='pics', null=True, blank=True)
    lender = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return "PA00" +str(self.id)

class Credit(models.Model):
    debtor = models.ForeignKey(Debtor, on_delete=models.SET_NULL, blank=True, null=True)    
    credit = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)    

class Deposit(models.Model):    
    deposit = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    credit = models.ForeignKey(Credit, on_delete=models.SET_NULL, blank=True, null=True)



    
 