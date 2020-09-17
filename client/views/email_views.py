from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..models.email_model import EmailManager, Emails
from ..models.user_model import User


def add_email(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'all_emails' : current_user.emails.all()
    }
    return render(request, 'new_email.html', context)

def new_email(request):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    errors = Emails.objects.email_validation(request.POST, request.session['user_id'])
    if len(errors) > 0:
        for key, error in errors.items():
            messages.error(request, error)
        return redirect('/add/email')
    current_user = User.objects.get(id = request.session['user_id'])
    Emails.objects.create(
        email = request.POST['email'],
        user = current_user
    )
    return redirect('/home')

def edit_email(request, email_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    email = Emails.objects.get(id=email_id)
    context = {
        'email' : email
    }
    return render(request, 'edit_email.html', context)

def process_edit_email(request, email_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    errors = Emails.objects.email_edit_validation(request.POST, request.session['user_id'], email_id)
    if len(errors) > 0:
        for key, error in errors.items():
            messages.error(request, error)
        return redirect(f'/edit/email/{email_id}')
    email = Emails.objects.get(id=email_id)
    email.email = request.POST['email']
    email.save()
    return redirect('/add/email')

def delete_email(request, email_id):
    if 'user_id' not in request.session:
        messages.error(request, "Must be logged in to access")
        return redirect('/login')
    email = Emails.objects.get(id=email_id)
    email.delete()
    return redirect('/add/email')