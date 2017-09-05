from django.shortcuts import render
from .models import Question, Answer, GLUser
# Create your views here.
from .tasks import checkAnswer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import *
def home(request):
    questions = Question.objects.all().order_by("-created")[:5]
    top10     = GLUser.objects.filter(score__gt=0).order_by('score')[:10]
    info ={
        'questions':questions,
        'top10':top10
    }
    return render(request,"index.html", info)

@login_required()
def codeEditor(request,question_id):
    question = Question.objects.get(id=question_id)
    info = {
        "question": question
    }
    if request.method == "POST":
        answer =    request.POST.get("answer",None)
        info['message'] = checkAnswer(question, request.user, answer)
    if question.type == 0: #Code
        return render(request, "TryitEditor.html",info)
    else: #Text
        top10 = GLUser.objects.filter(score__gt=0).order_by('-score')[:10]
        info['top10'] = top10
        return render(request,'question_extra.html',info)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        nextUrl  = request.GET.get("next", "/")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            gluser, created = GLUser.objects.get_or_create(user=request.user)
            if created:
               gluser.save()
            return HttpResponseRedirect(nextUrl)
    return render(request,"login.html")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def profile(request, username):
    return render(request, "profile.html")