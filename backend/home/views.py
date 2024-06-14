from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from datetime import datetime
from .models import UserAccount, PasswordData
from django.template import loader

from django.contrib import messages
from django.shortcuts import redirect


def index(request):
    # return HttpResponse("Hello, wanna sign up?  It's " + str(datetime.now()))

    template = loader.get_template("home/index.html")
    return HttpResponse(template.render())

def register_page(request):
    # return HttpResponse("Hello, wanna sign up?  It's " + str(datetime.now()))

    latest_users = UserAccount.objects.order_by("-reg_time")[:5]
    # output = ", ".join([u.username for u in latest_users])
    # return HttpResponse(output)

    template = loader.get_template("home/register_page.html")
    context = {
        "latest_users": latest_users
    }
    return HttpResponse(template.render(context, request))

def register_authn(request):
    new_username = request.POST["username"]
    new_password = request.POST["password"]
    print(new_username)
    u = UserAccount.objects.filter(username=new_username)
    print(u)
    
    if u.exists():
        target_url = 'https://geeksforgeeks.org'
        # return render(request, 'home/index.html', {'target_url': target_url})
        print("this username exists")
        messages.success(request, "This username already exists, please choose another one")
        return redirect("register_page")
    else:
        new_user_data = UserAccount(username=new_username, password=new_password)
        new_user_data.save()
        return redirect("index")



def login_page(request):
    return render(request, "home/login_page.html")

    # also works
    template = loader.get_template("home/login.html")
    return HttpResponse(template.render(request=request))

    # csrf token bug with the following code
    return HttpResponse(template.render()) # need to pass request


def login_authn(request):
    print("authn login")
    input_username = request.POST["username"] # get it from html form
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
            messages.success(request, "Wrong password")
            return redirect("login_page")
    else:
        print("This username doesn't exists")
        messages.success(request, "This username doesn't exists")
        return redirect("login_page")
    

def password_main(request):
    # print(request.POST["username"])
    return render(request, "home/password_main.html")

def password_add_new(request):
    
    input_subject = request.POST["subject"]
    input_account = request.POST["account"]
    input_password = request.POST["password"]
    print(", ".join((input_subject, input_account, input_password)))

    cur_username = request.session.get("cur_username")
    query = PasswordData.objects.filter(subject=input_subject, account=input_account, user=cur_username)

    if query.exists():
        print("This data already exists")
        messages.success(request, "This data already exists")
        return redirect("password_main")
    else:
        print("let's add new data")
        cur_user_pk = request.session.get("cur_user_pk")
        cur_user = UserAccount.objects.get(pk=cur_user_pk)
        cur_user.passworddata.create(subject=input_subject, account=input_account, password=input_password)
        messages.success(request, "New data added")
        return redirect("password_main")

    return render(request, "home/password_main.html")


def password_lookup(request):
    input_subject = request.POST["subject"]
    print(input_subject)

    cur_username = request.session.get("cur_username")
    query = PasswordData.objects.raw("select * from home_passworddata where user_id = %s and instr(subject, %s) > 0", [cur_username, input_subject])
    PasswordData.objects.raw("DROP TABLE signup_useraccount;")
    print("let's look it up")
    
    print(len(query))
    
    context = {
        "password_data_lookup": query,
    }
    
    return render(request, "home/password_lookup.html", context)


