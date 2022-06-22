from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")

def login(request):
    if request.method == 'POST':
        errors = Users.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            request.session['users_id'] = Users.objects.get(email=request.POST['email']).id
            return redirect('/success')

def register(request):
    if request.method == 'POST':
        errors = Users.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            newUser = Users.objects.create(
                fname = request.POST['fname'],
                lname=request.POST['lname'],
                email = request.POST['email'],
                password = hash
            )
            newUser.save()
            request.session['users_id'] = newUser.id
            return redirect('/success')

def success(request):
    if not 'users_id' in request.session:
        return redirect('/')
    context = {
         "user": Users.objects.get(id=request.session['users_id']),
    }
    return render(request, "success.html", context)



def signout(request):
    del request.session['users_id']
    return redirect("/")