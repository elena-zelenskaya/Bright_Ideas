from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    request.session.flush()
    return render(request, 'index.html')

def home(request):
    request.session.flush()
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
            if "avatar" in request.FILES:
                avatar = request.FILES["avatar"]
                new_user.avatar = avatar
                new_user.save()
            request.session['userid'] = new_user.id
            return redirect("/bright-ideas/")
    request.session.flush()
    return redirect("/")

def login_user(request):
    if request.method == "POST":
        email = request.POST["email_login"]
        password = request.POST["password_login"]
        if not User.objects.authenticate(email, password):
            messages.error(request, "Email and Password do not match", extra_tags='login')
            return redirect("/")
        else:
            user = User.objects.get(email=email)
            request.session["userid"] = user.id
            return redirect('/bright-ideas/')
    request.session.flush()
    return redirect("/")

def logout_user(request):
    request.session.flush()
    return redirect("/")

def view_user(request, user_id): 
    context = {
		"user": User.objects.get(id = user_id)
	}
    return render(request, 'user_info.html', context)

