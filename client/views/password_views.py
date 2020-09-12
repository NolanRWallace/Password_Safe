from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..models.user_model import User
from ..models.password_model import Passwords
from password_safe.settings import PASSWORD_KEY
from ..security import encrypt, decrypt

def add_password(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    current_user = User.objects.get(id=request.session['user_id'])
    all_passwords = current_user.passwords.all()
    decrypted_pass = {}
    for password in all_passwords:
        decrpyted = decrypt(password.password)
        decrypted_pass[password.id] = decrpyted
    context = {
        'all_passwords' : decrypted_pass,
    }
    return render(request, 'new_password.html', context)

def new_password(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    if request.POST['password'] != request.POST['confirm_pw']:
        messages.error(request, "Passwords do not match, try again")
        return redirect('/add/password')
    current_user = User.objects.get(id = request.session['user_id'])
    all_passwords = Passwords.objects.filter(user=current_user)
    for password in all_passwords:
        if request.POST['password'] == password.password:
            messages.error(request, "That Password already exist")
            return redirect('/add/password')
    encrypted_password = encrypt(request.POST['password'])
    Passwords.objects.create(
        password = encrypted_password,
        user = current_user
    )
    return redirect('/home')

def edit_password(request, pass_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    password = Passwords.objects.get(id=pass_id)
    decrypted_pass = decrypt(password.password)
    context = {
        'password' : decrypted_pass,
        'id' : password.id
    }
    return render(request, 'edit_password.html', context)

def process_edit_password(request, pass_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    if request.POST['password'] != request.POST['confirm_pw']:
        messages.error(request, "Passwords do not match, try again")
        return redirect(f'/edit/password/{pass_id}')
    password = Passwords.objects.get(id=pass_id)
    password.password = encrypt(request.POST['password'])
    password.save()
    return redirect('/add/password')

def delete_password(request, pass_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    password = Passwords.objects.get(id=pass_id)
    password.delete()
    return redirect('/add/password')