from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "app/Dashboard.html")
    else:
        return redirect("login")

@login_required(login_url='login')
def loan(request):

    return render(request, "app/loan.html")

@login_required(login_url='login')
def debtor(request):
    debtors = Debtor.objects.filter(lender_id=request.user.id)        
    return render(request, "app/debtor.html",{
        "debtors": debtors,
    })

@login_required(login_url='login')
def newdebtor(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']

        new_debtor = Debtor.objects.create(debtorName=name, phone=phone, address=address, lender=request.user)
        new_debtor.save()
        return redirect("debtor")
    else:
        return render(request, "app/newdebtor.html")

# @login_required(login_url='login')
def debtorprofile(request, id):
    profile = Debtor.objects.get(id=id)

    return render(request, "app/debtorprofile.html",{
        "profile":profile,
    })

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