from django.db import models
from django.contrib.auth.models import User
import os
import datetime
from PIL import Image
from django.conf import settings
import os

# loan
class Debtor(models.Model):
    debtorName = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null= True)
    address = models.TextField(blank=True, null= True)
    img = models.ImageField(default='avatar.png', upload_to='pics')    
    lender = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    totalbalance = models.FloatField(default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        pic = Image.open(self.img.path)	
        size = 250, 250
        pic.thumbnail(size, Image.LANCZOS)
        pic.save(self.img.path) 


    def __str__(self):
        return "PA00" +str(self.id)

class Account(models.Model):
    debtor = models.ForeignKey(Debtor, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null= True)
    loan = models.FloatField(default=0, null=True, blank=True)
    deposit = models.FloatField(default=0, null=True, blank=True)
    balance = models.FloatField(default=0, null=True, blank=True)
    date = models.DateField( default=datetime.date.today, blank=True, null=True)
    status = models.BooleanField(default=None, null=True, blank=False)
    
# Invest
class Lender(models.Model):
    lenderName = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null= True)
    address = models.TextField(blank=True, null= True)
    img = models.ImageField(default='avatar.png', upload_to='pics')
    investor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    totalbalance = models.FloatField(default=0, null=True, blank=True)   

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        pic = Image.open(self.img.path)	
        
        size = 250, 250
        pic.thumbnail(size, Image.LANCZOS)
        pic.save(self.img.path) 
    
    def __str__(self):
        return "IV00" +str(self.id)

class Invest(models.Model):
    lender = models.ForeignKey(Lender, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null= True)
    invest = models.FloatField(default=0, null=True, blank=True)
    retern = models.FloatField(default=0, null=True, blank=True)
    balance = models.FloatField(default=0, null=True, blank=True)
    date = models.DateField( default=datetime.date.today)
    status = models.BooleanField(default=False, null=True, blank=False)        

class Landowner(models.Model):    
    Landownername = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null= True)
    img = models.ImageField(default='avatar.png', upload_to='pics')
    landbuyer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=None, null=True, blank=False)   

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        pic = Image.open(self.img.path)	
        
        size = 250, 250
        pic.thumbnail(size, Image.LANCZOS)
        pic.save(self.img.path) 

    def __str__(self):
        return "LD00" + str(self.id)

class Land(models.Model):
    landowner = models.ForeignKey(Landowner, on_delete=models.SET_NULL, blank=True, null=True)
    landQTY = models.FloatField(default=0, null=True, blank=True)
    rsdag = models.CharField(max_length=50)
    perDprice = models.FloatField(default=0, null=True, blank=True)
    mouja = models.CharField(max_length=50)

    def totalprice(self):
        return self.perDprice * self.landQTY
    
class Advance(models.Model):
    land = models.ForeignKey(Land, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField( default=datetime.date.today)
    description = models.TextField(blank=True, null= True)
    advance = models.FloatField(default=0, null=True, blank=True)