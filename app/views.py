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
    profile = Debtor.objects.filter(lender=request.user.id).all()    
    accounts = Account.objects.filter(debtor__in=profile).order_by('-date')

    
    return render(request, "app/loan.html",{
        "accounts":accounts,
    })

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

@login_required(login_url='login')
def debtorprofile(request, id):
    profile = Debtor.objects.get(id=id)
    account = Account.objects.filter(debtor=profile).order_by('date')

    # print(account[0].balance)
    return render(request, "app/debtorprofile.html",{
        "profile": profile,
        "accounts": account,
    })

@login_required(login_url='login')
def accounts(request, id, string):
    profile = Debtor.objects.get(id=id)
    account = Account.objects.filter(debtor=profile).last()

    if account == None:
        balance = 0
    else:
        balance = account.balance 

    if request.method == 'POST':
        if string == 'loan':            
            loan = request.POST['loan']            
            balance = int(loan) + balance
            deposit = 0
        else:            
            loan = 0
            deposit = request.POST['deposit']            
            balance = balance - int(deposit)
        
        description = request.POST['description']
        date = request.POST['date']
        
        ac = Account.objects.create(debtor=profile, description=description, loan=loan, deposit=deposit, balance = balance, date=date)
        ac.status = True if balance == 0 else False        
        ac.save()        
        
        return redirect("debtorprofile", id)
    else:
        return render(request, "app/loanform.html")



@login_required(login_url='login')
def invest(request):
    profile = Lender.objects.filter(investor=request.user.id).all()    
    accounts = Invest.objects.filter(lender__in=profile).order_by('-date')

    
    return render(request, "app/invest.html",{
        "accounts":accounts,
    })

@login_required(login_url='login')
def newlender(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']

        new_lender = Lender.objects.create(lenderName=name, phone=phone, address=address, investor=request.user)
        new_lender.save()
        return redirect("debtor")
    else:
        return render(request, "app/newlender.html")

@login_required(login_url='login')
def lender(request):
    lenders = Lender.objects.filter(investor_id=request.user.id)        
    return render(request, "app/lender.html",{
        "lenders": lenders,
    })

@login_required(login_url='login')
def lenderprofile(request, id):
    profile = Lender.objects.get(id=id)
    account = Invest.objects.filter(lender=profile).order_by('date')

    # print(account[0].balance)
    return render(request, "app/lenderprofile.html",{
        "profile": profile,
        "accounts": account,
    })

@login_required(login_url='login')
def lenderaccounts(request, id, string):
    profile = Lender.objects.get(id=id)
    account = Invest.objects.filter(lender=profile).last()

    if account == None:
        balance = 0
    else:
        balance = account.balance 

    if request.method == 'POST':
        if string == 'loan':            
            loan = request.POST['loan']            
            balance = int(loan) + balance
            deposit = 0
        else:            
            loan = 0
            deposit = request.POST['deposit']            
            balance = balance - int(deposit)
        
        description = request.POST['description']
        date = request.POST['date']
        
        ac = Invest.objects.create(lender=profile, description=description, invest=loan, retern=deposit, balance = balance, date=date)
        ac.status = True if balance == 0 else False        
        ac.save()        
        
        return redirect("lenderprofile", id)
    else:
        return render(request, "app/loanform.html")

@login_required(login_url='login')
def land(request):
    landowners = Landowner.objects.filter(landbuyer_id=request.user.id)
    print("this", landowners)

    return render(request, "app/landdetails.html",{
        "landowners": landowners,
    })

@login_required(login_url='login')
def newland(request, id):
    if request.method == "POST":
        mouja = request.POST['mouja']
        rsdag = request.POST['rsdag']
        landQTY = request.POST['landQTY']
        perDprice = request.POST['perDprice']

        newland = Land.objects.create(landowner_id=id, mouja=mouja, rsdag=rsdag, landQTY=landQTY, perDprice=perDprice)
        newland.save()

    return redirect("landownerprofile", id)

@login_required(login_url='login')
def newlandowner(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']

        new_Landowner = Landowner.objects.create(Landownername=name, phone=phone, landbuyer=request.user)
        new_Landowner.save()

        return redirect("land")
    else:
        return render(request, "app/newlandowner.html")
 

@login_required(login_url='login')
def landownerprofile(request, id):
    profile = Landowner.objects.get(id=id)    
    lands = Land.objects.filter(landowner=profile)
    
    landdetails = {}
    for land in lands:
        advance = Advance.objects.filter(land=land)
        landdetails[land] = advance

    return render(request, "app/landownerprofile.html",{
        "profile": profile,
        "landdetails": landdetails,
    })

@login_required(login_url='login')
def advance(request, id, landid):
    print(id, landid)
    if request.method == 'POST':
         advance = request.POST['advance']
         description = request.POST['description']
         date = request.POST['date']

    # lands = Land.objects.get(landowner=landid)
    advance = Advance.objects.create(land_id=landid, description=description, advance=advance, date=date)
    advance.save()

    return redirect("landownerprofile", id)

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