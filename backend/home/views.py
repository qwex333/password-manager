from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from datetime import datetime
from .models import PasswordData
from django.template import loader

from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def index(request):
    # return HttpResponse("Hello, wanna sign up?  It's " + str(datetime.now()))

    template = loader.get_template("home/index.html")
    return HttpResponse(template.render(request=request)) # need to pass request to ge prompt message

def register_page(request):
    return render(request, "home/register_page.html")
    # return HttpResponse("Hello, wanna sign up?  It's " + str(datetime.now()))

    latest_users = User.objects.order_by("-date_joined")[:5]
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
    u = User.objects.filter(username=new_username)
    print(u)
    
    if u.exists():
        print("this username exists")
        messages.success(request, "This username already exists, please choose another one")
        return redirect("register_page")
    else:
        # new_user = User(username=new_username, password=new_password) # this will not encrypt password
        new_user = User.objects.create_user(username=new_username, password=new_password)
        new_user.save()

        messages.success(request, "Account registered!")
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
    
    user = authenticate(request, username=input_username, password=input_password)
    
    if user is not None:
        print("password matches")
        login(request, user)
        # request.session["cur_user_pk"] = user.pk
        messages.success(request, "login succeeds")
        return redirect("password_main")
    else:
        print("Wrong user name or password")
        messages.success(request, "Wrong user name or password")
        return redirect("login_page")
    

def password_main(request):
    # print(request.POST["username"])
    return render(request, "home/password_main.html")

def password_add_new(request):
    
    input_subject = request.POST["subject"]
    input_account = request.POST["account"]
    input_password = request.POST["password"]
    print(", ".join((input_subject, input_account, input_password)))

    cur_user = request.user
    query = cur_user.passworddata.filter(subject=input_subject, account=input_account)
    print(len(query))

    if query.exists():
        print("This data already exists")
        messages.success(request, "This data already exists")
        return redirect("password_main")
    else:
        print("let's add new data")
        cur_user_pk = request.session.get("cur_user_pk")
        cur_user.passworddata.create(subject=input_subject, account=input_account, password=input_password)

        messages.success(request, "New data added")
        return redirect("password_main")


def password_lookup(request):
    cur_user = request.user

    if "subject" in request.POST:
        print("yes")
        input_subject = request.POST["subject"]
        print(input_subject)
        query = PasswordData.objects.raw("select * from home_passworddata where user_id = %s and instr(subject, %s) > 0", [cur_user.id, input_subject])
    else:
        print("no")
        query = cur_user.passworddata.all()


    print("length: ", len(query))
    
    context = {
        "password_data_lookup": query,
    }
    
    return render(request, "home/password_lookup.html", context)

def password_list_all(request):
    cur_user = request.user

