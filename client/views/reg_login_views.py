from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..models.user_model import User, UserManager
from ..models.combo_model import Combo
from ..security import encrypt, decrypt
import bcrypt



def index(request):
    return redirect('/registration')

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
    User.objects.create(
        f_name = request.POST['f_name'],
        l_name = request.POST['l_name'],
        email = request.POST['email'],
        password = bcrypt.hashpw(password, bcrypt.gensalt()).decode(),
    )
    new_user = User.objects.filter(email=request.POST['email'])
    new_user = new_user[0]
    request.session['user_id'] = new_user.id
    request.session['user_name'] = new_user.f_name + ' ' + new_user.l_name
    return redirect('/home')

def home(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    current_user = User.objects.get(id=request.session['user_id'])
    all_combos = current_user.combos.all()
    decrypted_combos = {}
    for combo in all_combos:
        decrpyted = decrypt(combo.password.password)
        decrypted_combos[combo.id] = [combo.accountName, combo.email.email, decrpyted]
    context = {
        'all_combos' : decrypted_combos,
    }
    return render(request, 'home.html', context)

def logout(request):
    request.session.flush()
    return redirect('/login')
    