from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..models import User, Combo, Emails, Passwords
import bcrypt

def index(request):
    return redirect('/login')

def login_form(request):
    return render(request, 'login.html')

def login(request):
    login_user = User.objects.filter(email=request.POST['email'])
    if login_user:
        login_user = login_user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), login_user.password.encode()):
            request.session['user_id'] = login_user.id
            request.session['user_name'] = login_user.f_name + ' ' + login_user.l_name
            return redirect('/home')
        else: 
            messages.error(request, "Password is incorrect")
    else:
        messages.error(request, "Email does not exist")
    return redirect('/login')

def reg_form(request):
    return render(request, 'registration.html')

def reg(request):
    errors = User.objects.reg_validation(request.POST)
    if len(errors) > 0:
        for key, error in errors.items():
            messages.error(request, error)
        return redirect('/registration')
    password = request.POST['password'].encode('utf-8')
    confirm_pw = request.POST['confirm_pw'].encode('utf-8')
    User.objects.create(
        f_name = request.POST['f_name'],
        l_name = request.POST['l_name'],
        email = request.POST['email'],
        password = bcrypt.hashpw(password, bcrypt.gensalt()).decode(),
        confirm_pw = bcrypt.hashpw(confirm_pw, bcrypt.gensalt()).decode(),
    )
    new_user = User.objects.filter(email=request.POST['email'])
    new_user = new_user[0]
    request.session['user_id'] = new_user.id
    request.session['user_name'] = new_user.f_name + ' ' + new_user.l_name
    return redirect('/home')