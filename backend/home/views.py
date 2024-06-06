from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from datetime import datetime
from .models import UserAccount, PasswordData
from django.template import loader

# from django.contrib import messages
from django.shortcuts import redirect

def index(request):
    # return HttpResponse("Hello, wanna sign up?  It's " + str(datetime.now()))

    template = loader.get_template("home/index.html")
    return HttpResponse(template.render())

def register(request):
    # return HttpResponse("Hello, wanna sign up?  It's " + str(datetime.now()))

    latest_users = UserAccount.objects.order_by("-reg_time")[:5]
    # output = ", ".join([u.username for u in latest_users])
    # return HttpResponse(output)

    template = loader.get_template("home/register.html")
    context = {
        "latest_users": latest_users
    }
    return HttpResponse(template.render(context, request))

def authenticate_reg(request):
    new_username = request.POST["username"]
    new_password = request.POST["password"]
    print(new_username)
    u = UserAccount.objects.filter(username=new_username)
    print(u)
    
    if u.exists():
        target_url = 'https://geeksforgeeks.org'
        # return render(request, 'home/index.html', {'target_url': target_url})
        print("this username exists")
        return redirect("register")
    else:
        new_user_data = UserAccount(username=new_username, password=new_password)
        new_user_data.save()
        return redirect("index")



def login(request):
    return render(request, "home/login.html")

    # also works
    template = loader.get_template("home/login.html")
    return HttpResponse(template.render(request=request))

    # csrf token bug with the following code
    return HttpResponse(template.render()) # need to pass request


def authenticate_login(request):
    print("authn login")
    input_username = request.POST["username"]
    input_password = request.POST["password"]
    print(input_username)
    user_data = UserAccount.objects.filter(username=input_username)
    print(user_data)
    
    if user_data.exists():
        target_url = 'https://geeksforgeeks.org'
        # return render(request, 'home/index.html', {'target_url': target_url})

        print("great, this username exists")
        
        if input_password == user_data[0].password:
            print("password matches")
            request.session["cur_user_pk"] = user_data[0].pk
            return redirect("password_main")
        else:
            print("wrong password")
            return redirect("login")
    else:
        print("this username doesn't exists")
        return redirect("login")
    

def password_main(request):
    # print(request.POST["username"])
    return render(request, "home/password_main.html")

def password_add_new(request):
    cur_user_pk = request.session.get("cur_user_pk")
    
    input_subject = request.POST["subject"]
    input_account = request.POST["account"]
    input_password = request.POST["password"]
    print(", ".join((input_subject, input_account, input_password)))

    query = PasswordData.objects.filter(subject=input_subject, account=input_account)

    if query.exists():
        print("this data already exists")
        return redirect("password_main")
    else:
        print("let's add new data")
        cur_user = UserAccount.objects.get(pk=cur_user_pk)
        cur_user.passworddata.create(subject=input_subject, account=input_account, password=input_password)
        return redirect("password_main")

    return render(request, "home/password_main.html")


def password_lookup(request):
    input_subject = request.POST["subject"]
    print(input_subject)
    query = PasswordData.objects.raw("select * from home_passworddata where instr(subject, %s) > 0", [input_subject])
    print("let's look it up")
    
    print(len(query))
    
    context = {
        "password_data_lookup": query,
    }
    
    return render(request, "home/password_lookup.html", context)


