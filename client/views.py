from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Combo, Emails, Passwords
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

def home(request):
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'all_combos' : current_user.combos.all(),
    }
    return render(request, 'home.html', context)

def add_email(request):
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'all_emails' : current_user.emails.all()
    }
    return render(request, 'new_email.html', context)

def add_password(request):
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'all_passwords' : current_user.passwords.all()
    }
    return render(request, 'new_password.html', context)

def new_email(request):
    errors = Emails.objects.email_validation(request.POST)
    if len(errors) > 0:
        for key, error in errors.items():
            messages.error(request, error)
        return redirect('/add/email')
    elif request.POST['email'] != request.POST['confirm_email']:
        messages.error(request, "Emails do not match, check and resubmit")
        return redirect('/add/email')
    current_user = User.objects.filter(id = request.session['user_id'])
    Emails.objects.create(
        email = request.POST['email'],
        user = current_user[0]
    )
    return redirect('/home')

def new_password(request):
    if request.POST['password'] != request.POST['confirm_pw']:
        messages.error(request, "Passwords do not match, try again")
        return redirect('/new_data')
    current_user = User.objects.filter(id = request.session['user_id'])
    Passwords.objects.create(
        password = request.POST['password'],
        user = current_user[0]
    )
    return redirect('/home')

def new_combo(request):
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'all_emails' : current_user.emails.all(),
        'all_passwords' : current_user.passwords.all(),
    }
    return render(request, 'new_combo.html', context)

def add_combo(request):
    current_user = User.objects.get(id=request.session['user_id'])
    this_email = Emails.objects.get(id = request.POST['email'])
    this_password = Passwords.objects.get(id = request.POST['password'])
    Combo.objects.create(
        accountName = request.POST['accountName'],
        email = this_email,
        password = this_password,
        user = current_user
    )
    return redirect('/home')

def edit_combo(request, combo_id):
    current_user = User.objects.get(id=request.session['user_id'])
    combo = Combo.objects.get(id=combo_id)
    context = {
        'all_emails' : current_user.emails.exclude(email = combo.email.email),
        'all_passwords' : current_user.passwords.exclude(password = combo.password.password),
        'combo' : Combo.objects.get(id=combo_id),
    }
    return render(request, 'edit_combo.html', context)

def edit_email(request, email_id):
    # current_user = User.objects.get(id=request.session['user_id'])
    email = Emails.objects.get(id=email_id)
    context = {
        'email' : email
    }
    return render(request, 'edit_email.html', context)

def process_edit_email(request, email_id):
    email = Emails.objects.get(id=email_id)
    email.email = request.POST['email']
    email.save()
    return redirect('/add/email')

def delete_combo(request, combo_id):
    combo = Combo.objects.get(id=combo_id)
    combo.delete()
    return redirect('/home')

def delete_email(request, email_id):
    email = Emails.objects.get(id=email_id)
    email.delete()
    return redirect('/add/email')

def delete_password(request, pass_id):
    password = Passwords.objects.get(id=pass_id)
    password.delete()
    return redirect('/add/password')

def proccess_edit_combo(request, combo_id):
    # current_user = User.objects.get(id=request.session['user_id'])
    combo = Combo.objects.get(id=combo_id)
    this_email = Emails.objects.get(id = request.POST['email'])
    this_password = Passwords.objects.get(id = request.POST['password'])
    combo.password = this_password
    combo.accountName = request.POST['accountName']
    combo.email = this_email
    combo.save()
    return redirect('/home')

def logout(request):
    request.session.flush()
    return redirect('/login')
    