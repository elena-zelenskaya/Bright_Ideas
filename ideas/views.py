from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Idea
from users.models import User

# Create your views here.
def all_ideas(request):
    if 'userid' in request.session.keys():
        context = {
            'all_ideas': Idea.objects.all().order_by("-created_at"),
            'user': User.objects.get(id = request.session['userid'])
        }
        return render(request, 'ideas_wall.html', context)
    else:
        return HttpResponse("<h1>You are not logged in</h1>")

def create_idea(request):
    if request.method == "POST":
        description = request.POST["idea"]
        if len(description) == 0:
            messages.error(request, "Your message is empty!", extra_tags='empty_post')
            return redirect("../")
        user_id = request.session["userid"]
        user = User.objects.get(id=user_id)
        new_idea = Idea.objects.create(description = description, user = user)
        return redirect("../")

def idea_view(request, idea_id):
    pass

def delete_idea(request, idea_id):
    idea_to_delete = Idea.objects.get(id = idea_id)
    idea_to_delete.delete()
    return redirect("../")