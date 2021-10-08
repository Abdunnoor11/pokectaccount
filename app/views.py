from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from .models import *

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "app/Dashboard.html")
    else:
        return redirect("login")

def loan(request):
    return render(request, "app/loan.html")

def credit(request):
    if request.method == 'POST':
        name = request.POST['name']
        credit = request.POST['credit']

        new_credit = Credit.objects.create(nameDescription = name, credit = credit)
        new_credit.save()
        return redirect("loan")
    else:
        return render(request, "app/loanform.html")

def deposit(request):
    if request.method == 'POST':        
        creditid = request.POST['creditid']
        deposit = request.POST['deposit']
        print(creditid, deposit)
        # new_deposit = deposit.objects.create(nameDescription = creditid, credit = credit)
        # new_credit.save()
        return redirect("deposit")
    else:
        allcredit = Credit.objects.all()        
        return render(request, "app/depositform.html",{
            "allcredit": allcredit,
        })

def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']

        user = auth.authenticate(username=name, password = password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return redirect('login')
    else:
        return render(request, "app/login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')