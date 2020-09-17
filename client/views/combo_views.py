from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..models.user_model import User
from ..models.password_model import Passwords
from ..models.email_model import Emails
from ..models.combo_model import Combo
from ..security import encrypt, decrypt

def new_combo(request):
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
        'all_emails' : current_user.emails.all(),
        'all_passwords' : decrypted_pass,
    }
    return render(request, 'new_combo.html', context)

def add_combo(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    current_user = User.objects.get(id=request.session['user_id'])
    all_combos = Combo.objects.filter(user = current_user)
    for combo in all_combos:
        if combo.accountName.lower() == request.POST['accountName'].lower():
            messages.error(request, "Account already exist")
            return redirect('/new/combo')
    if request.POST['email'] == "None":
        messages.error(request, "Please Select an Email")
        return redirect('/new/combo')
    if request.POST['password'] == "None":
        messages.error(request, "Please Select a Password")
        return redirect('/new/combo')
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
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    current_user = User.objects.get(id=request.session['user_id'])
    combo = Combo.objects.get(id=combo_id)
    all_passwords = current_user.passwords.exclude(password = combo.password.password)
    this_password = {}
    this_password[combo.password.id] = decrypt(combo.password.password)
    decrypted_pass = {}
    for password in all_passwords:
        decrpyted = decrypt(password.password)
        decrypted_pass[password.id] = decrpyted
    context = {
        'all_emails' : current_user.emails.exclude(email = combo.email.email),
        'all_passwords' : decrypted_pass,
        'combo' : Combo.objects.get(id=combo_id),
        'this_password' : this_password
    }
    return render(request, 'edit_combo.html', context)

def delete_combo(request, combo_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    combo = Combo.objects.get(id=combo_id)
    combo.delete()
    return redirect('/home')

def proccess_edit_combo(request, combo_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    # current_user = User.objects.get(id=request.session['user_id'])
    combo = Combo.objects.get(id=combo_id)
    this_email = Emails.objects.get(id = request.POST['email'])
    this_password = Passwords.objects.get(id = request.POST['password'])
    combo.password = this_password
    combo.accountName = request.POST['accountName']
    combo.email = this_email
    combo.save()
    return redirect('/home')