from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    # request.session.flush()
    return render(request, 'index.html')

def home(request):
    return redirect("/main")

def all_users_emails():
    all_users_emails = []
    for user in User.objects.all():
        all_users_emails.append(user.email)
    return all_users_emails

def register_user(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.session, request.POST, all_users_emails())
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('/')
        else:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            alias = request.POST["alias"]
            email = request.POST["email"]
            password = request.POST["password"]
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(first_name = first_name, last_name = last_name, alias = alias, email = email, password = pw_hash)
            request.session['userid'] = new_user.id
            request.session['fname'] = new_user.first_name
            request.session['username'] = new_user.full_name
            request.session['alias'] = new_user.alias
            return redirect("/bright-ideas/")

def login_user(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.session, request.POST, all_users_emails())
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='login')
            return redirect('/')
        user = User.objects.get(email=request.POST['email_login'])

        if bcrypt.checkpw(request.POST['password_login'].encode(), user.password.encode()):
            request.session['userid'] = user.id
            request.session['fname'] = user.first_name
            request.session['username'] = user.full_name
            request.session['alias'] = user.alias
            return redirect('/bright-ideas/')
        else:
            messages.error(request, 'Wrong password', extra_tags='login')
            return redirect("/")

def logout_user(request):
    request.session.flush()
    return redirect("/")

def view_user(request, user_id): 
    context = {
		"user": User.objects.get(id = user_id)
	}
    return render(request, 'user_info.html', context)

