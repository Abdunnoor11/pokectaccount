from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import *
import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # for loan
        accounts = Account.objects.filter(debtor_id = request.user.id)
        total_loan = 0
        total_deposit = 0
        total_due_loan = 0
        
        total_loan, total_deposit, total_due_loan = total_count_debtor(accounts)
        
        # for invest
        invests = Invest.objects.filter(lender_id = request.user.id)
        
        total_invest, total_return, total_due_invest = total_count_lender(invests)

        #  For Land
        Landowners = Landowner.objects.filter(landbuyer=request.user.id) 
        
        land = Land.objects.filter(landowner__id__in=Landowners.all())
        total_land_price = sum([i.totalprice() for i in land])
        
        advanced = Advance.objects.filter(land__id__in = land.all())
        total_advanced = sum([i.advance for i in advanced])
        print(total_advanced)
        
        return render(request, "app/Dashboard.html",{
            # loan
            "total_loan": total_loan,
            "total_deposit": total_deposit,
            "total_due_loan": total_due_loan,
            # invest
            "total_invest": total_invest,
            "total_return": total_return,
            "total_due_invest": total_due_invest,
            # Land
            "total_land_price":total_land_price,
            "total_advanced":total_advanced,
            "total_due":total_land_price-total_advanced,
        })
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
def loanmenu(request):
    return render(request, "app/loanmenu.html")

@login_required(login_url='login')
def debtor(request):
    debtors = Debtor.objects.filter(lender_id=request.user.id)

    d = {}
    for debtor in debtors:
        accounts = Account.objects.filter(debtor=debtor)
        a, b, c = total_count_debtor(accounts)
        if c == 0:
            status = "paid"
        elif c > 0:
            status = "Due"
        else:
            status = "None"  

        d[debtor] = c, status

    return render(request, "app/debtor.html",{
        "debtors": d,        
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
    if request.method == 'POST' and request.FILES['img']:
        i = request.FILES['img']    

        profile = Debtor.objects.get(id=id)
        profile.img = i        
        profile.save()

        return redirect("debtorprofile", id)
    
    else:
        profile = Debtor.objects.get(id=id)        
        accounts = Account.objects.filter(debtor=profile).order_by('date')    
        
        total_loan, total_depost, b = total_count_debtor(accounts)

        return render(request, "app/debtorprofile.html",{
            "profile": profile,
            "accounts": accounts,
            "total_loan": total_loan,
            "total_deposit": total_depost,
            "Due": b,      
        })

def total_count_debtor(accounts):
    total_loan = 0
    total_depost = 0
    b = 0

    for account in accounts:
        total_loan = total_loan + account.loan
        total_depost = total_depost + account.deposit

    b = total_loan - total_depost
    return total_loan, total_depost, b

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
            balance = float(loan) + balance
            deposit = 0
        else:
            loan = 0
            deposit = request.POST['deposit']
            
            if float(deposit) > balance:
                messages.add_message(request, messages.WARNING, 'insufficient balance.')
                return redirect("debtorprofile", id)

            balance = balance - float(deposit)            
        
        description = request.POST['description']
        date = request.POST['date']
        
        if len(date) == 0:
            d = datetime.datetime.now()
        else:
            d = datetime.datetime.strptime(date, "%Y-%m-%d").date()


        ac = Account.objects.create(debtor=profile, description=description, loan=loan, deposit=deposit, balance = balance, date=d)
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
def investmenu(request):
    return render(request, "app/investmenu.html")

@login_required(login_url='login')
def newlender(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']

        new_lender = Lender.objects.create(lenderName=name, phone=phone, address=address, investor=request.user)
        new_lender.save()
        return redirect("lender")
    else:
        return render(request, "app/newlender.html")

@login_required(login_url='login')
def lender(request):
    lenders = Lender.objects.filter(investor_id=request.user.id) 

    d = {}
    for lender in lenders:
        accounts = Invest.objects.filter(lender=lender)
        a, b, c = total_count_lender(accounts)
        if c == 0:
            status = "paid"
        elif c > 0:
            status = "Due"
        else:
            status = "None"  

        d[lender] = c, status  

    return render(request, "app/lender.html",{
        "lenders": d,
    })

@login_required(login_url='login')
def lenderprofile(request, id):
    if request.method == 'POST' and request.FILES['img']:
        i = request.FILES['img']    

        profile = Lender.objects.get(id=id)
        profile.img = i        
        profile.save()

        return redirect("lenderprofile", id)

    else:
        profile = Lender.objects.get(id=id)
        accounts = Invest.objects.filter(lender=profile).order_by('date')

        total_invest, total_return, b = total_count_lender(accounts)

        return render(request, "app/lenderprofile.html",{
            "profile": profile,
            "accounts": accounts,
            "total_return": total_return,
            "total_invest": total_invest,
            "Due": b,
        })

def total_count_lender(accounts):
    total_invest = 0
    total_return = 0
    b = 0

    for account in accounts:
        total_invest = total_invest + account.invest
        total_return = total_return + account.retern

    b = total_invest - total_return

    return total_invest, total_return, b

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
            balance = float(loan) + balance
            deposit = 0
        else:            
            loan = 0
            deposit = request.POST['deposit']          
            
            if float(deposit) > balance:
                messages.add_message(request, messages.WARNING, 'insufficient balance.')
                return redirect("lenderprofile", id)

            balance = balance - float(deposit)
        
        description = request.POST['description']
        date = request.POST['date']
        
        if len(date) == 0:
            d = datetime.datetime.now()
        else:
            d = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        ac = Invest.objects.create(lender=profile, description=description, invest=loan, retern=deposit, balance = balance, date=d)
        ac.status = True if balance == 0 else False        
        ac.save()        
        
        return redirect("lenderprofile", id)
    else:
        return render(request, "app/loanform.html")

@login_required(login_url='login')
def land(request):
    landowners = Landowner.objects.filter(landbuyer_id=request.user.id)    
    
    return render(request, "app/landdetails.html",{
        "landowners": landowners,
    })

def landmenu(request):    
    return render(request, "app/landmenu.html")

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
    if request.method == 'POST' and request.FILES['img']:
        i = request.FILES['img']    

        profile = Landowner.objects.get(id=id)
        profile.img = i        
        profile.save()

        return redirect("landownerprofile", id)
    
    else:        
        profile = Landowner.objects.get(id=id)    
        lands = Land.objects.filter(landowner=profile)
        
        landdetails = {}

        for land in lands:
            advance = Advance.objects.filter(land=land)
            total = sum([a.advance for a in advance])
            balacnce = land.totalprice() - total
            landdetails[land] = total, balacnce
        

        return render(request, "app/landownerprofile.html",{
            "profile": profile,
            "landdetails": landdetails,
        })


@login_required(login_url='login')
def advance(request, id, landid):    

    if request.method == 'POST':
        advance = request.POST['amount']
        description = request.POST['description']        
        date = request.POST['date']
            
        if len(date) == 0:
            d = datetime.datetime.now()
        else:
            d = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        land = Land.objects.get(id=landid)  
        advances = Advance.objects.filter(land_id=landid)
        total = sum([a.advance for a in advances])
        balance = land.totalprice() - total

        if balance >= float(advance):
            advance = Advance.objects.create(land_id=landid, description=description, advance=advance, date=d)
            advance.save()
            return redirect('landownerprofile', id)
        else:
            messages.add_message(request, messages.WARNING, 'insufficient balance.')
            return redirect('advancepage', id, landid)
            

@login_required(login_url='login')
def advancepage(request, id, landid):    

    land = Land.objects.get(id=landid)      
    
    advance = Advance.objects.filter(land=land)
    total = sum([a.advance for a in advance])
    balance = land.totalprice() - total       
    
    advances = Advance.objects.filter(land_id=landid)       


    return render(request, "app/advancepage.html",{
        "land":land,        
        "total":total,
        "balacnce":balance,
        "advances": advances,
        "id":id,   
    })

def landCencellation(request, id, landid):
    land = Land.objects.get(id=landid)      
    land.delete()
    advance = Advance.objects.filter(land=land).delete()

    return redirect('landownerprofile', id)

def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']

        user = auth.authenticate(username=name, password = password)        
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.add_message(request, messages.WARNING, 'User not found!!!')
            return redirect('login')            
    else:
        return render(request, "app/login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')