from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Idea
from users.models import User

# Create your views here.
def all_ideas(request):
    if 'userid' in request.session.keys():
        context = {
            'all_ideas': Idea.objects.all().order_by("-number_of_likes"),
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

def view_idea(request, idea_id):
    context = {
		"idea": Idea.objects.get(id = idea_id),
	}
    return render(request, 'view_idea.html', context)

def delete_idea(request, idea_id):
    idea_to_delete = Idea.objects.get(id = idea_id)
    idea_to_delete.delete()
    return redirect("../../")

def create_like(request, idea_id):
    user = User.objects.get(id = request.session['userid'])
    idea_to_edit = Idea.objects.get(id = idea_id)
    if idea_to_edit in user.ideas.all():
        messages.error(request, "You already liked this idea", extra_tags='no_more_likes')
        return redirect("../../")
    else:
        idea_to_edit.number_of_likes += 1
        idea_to_edit.save()
        user.ideas.add(idea_to_edit)
        return redirect("../../")
    