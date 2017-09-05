# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from models import *

from datetime import datetime

def home(request):
    devs = Developer.objects.order_by('?')[:3]
    return render(request, 'windows/home.html', {'devs': devs})

@login_required
def scoreboard(request):
    devs = Developer.objects.order_by('-scores')[:10]
    return render(request, 'windows/scoreboard.html', {'devs': devs})

@login_required
def quiz(request):
    answered = 0
    correct = incorrect = False
    questions = Quiz.objects.count()
    if request.user.is_authenticated:
        if request.method == 'GET':
            quiz = Quiz.objects.order_by('?')[0]
            return render(request, 'windows/quiz.html', {'answered' : answered, 'questions': questions, 'quiz' : quiz})
        else:
            quiz_id = request.POST.get('quiz_id')
            result = request.POST.get('result')
            answer = request.POST.get('answer')
            did_answer = request.POST.get('did_answer')

            try:
                quiz = Quiz.objects.get(pk=quiz_id)
                if result == 'OK':
                    if answer == quiz.answer:
                        correct = True
                    else :
                        incorrect = True
                elif result == answer:
                    correct = True
                else:
                    incorrect = True
            except ObjectDoesNotExist:
                pass

            return render(request, 'windows/quiz.html', {'answered': answered, 'questions': questions, 'quiz': quiz, 'correct': correct, 'incorrect': incorrect})

@login_required
def team(request, team_id):
    teams = team = None
    if team_id == 'all':
        teams = Team.objects.all()
    else:
        team = Team.objects.get(pk=team_id)
    return render(request, 'windows/team.html', {'teams': teams, 'team': team})

@login_required
def sendreport(request):
    response_data = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            general = request.POST.get('general')
            achievement = request.POST.get('achievement')
            planning = request.POST.get('planning')
            trouble = request.POST.get('trouble')
            try:
                dev = request.user.developer
                if dev.reports.count() == 0:
                    report = Report(name=dev.name, general=general, achievement=achievement, plan=planning,
                                    trouble=trouble)
                    report.week = date.today().isocalendar()[1]
                    report.save()
                    dev.reports.add(report)
                else:
                    last_report = dev.reports.order_by('-week')[0]

                    report = Report(name=dev.name, general=general, achievement=achievement, plan=planning,
                                    trouble=trouble)
                    report.week = last_report.week + 1
                    report.save()
                    dev.reports.add(report)
                dev.save()
                response_data['success'] = 'Success, your reports are submit to server'
            except ObjectDoesNotExist:
                response_data['error'] = 'Sorry, you are not Windows user'
        else:
            response_data['success'] = 'Sorry, please login before sending reports'

    response_data['devs'] = Developer.objects.order_by('name')
    response_data['teams'] = Team.objects.all()
    return render(request, "windows/report.html", response_data)

@login_required
def report(request):
    if request.method == "POST":
        response_data = {}
        try:
            dev_id = request.POST.get('dev_id', '')
            team_id = request.POST.get('team_id', '')

            if dev_id != '':
                dev = Developer.objects.get(pk=dev_id)
                reports = []
                for report in dev.reports.order_by('-week'):
                    r = {}
                    r['date'] = str(report.week)
                    r['general'] = report.general
                    r['planning'] = report.plan
                    r['achievement'] = report.achievement
                    r['trouble'] = report.trouble
                    reports.append(r)
                response_data['message'] = reports
            elif team_id != '':
                team = Team.objects.get(pk=team_id)
                devs = []
                for dev in team.developer_set.all():
                    if dev.reports.count() > 0:
                        report = dev.reports.order_by('-week')[0]
                        r = {}
                        r['dev'] = report.name + ' - ' + str(report.week)
                        r['general'] = report.general
                        r['planning'] = report.plan
                        r['achievement'] = report.achievement
                        r['trouble'] = report.trouble
                        devs.append(r)
                response_data['message'] = devs

        except ObjectDoesNotExist:
            response_data['message'] = 'Sorry, this user does not found'

        return JsonResponse(response_data)
    else:
        devs = Developer.objects.order_by('name')
        teams = Team.objects.all()
        return render(request, "windows/report.html", {'devs': devs, 'teams': teams})

@login_required
def bem(request, bem_id):
    if request.method == 'POST':
        response_data = {}
        if request.user.is_authenticated:
            try:
                bem_id = request.POST.get('bem_id')
                dev = request.user.developer
                bem = get_object_or_404(Bem, pk=bem_id)
                response_data['bem'] = bem
                voted = False

                if bem.expired == True:
                    response_data['error'] = 'Sorry, Bem is over'
                elif dev.team.name == bem.dev.team.name:
                    if dev.vote_team == True:
                        response_data['error'] = 'Sorry, you already voted for your team member'
                    else:
                        dev.vote_team = True
                        if bem.vote != None:
                            vote = bem.vote

                            for user in vote.users.all():
                                if dev.name == user.name:
                                    voted = True
                                    response_data['error'] = 'Sorry, you already voted for this member'
                                    break
                            if voted == False:
                                vote.users.add(dev)
                                vote.save()
                                dev.vote_count += 1
                                dev.save()
                                response_data['success'] = 'Success, your vote was submitted to server'
                        else:
                            vote = Vote()
                            vote.save()
                            vote.users.add(dev)
                            bem.vote = vote
                            bem.save()
                            dev.vote_count += 1
                            dev.save()
                            voted = True
                            response_data['success'] = 'Success, your vote is submit to server'
                elif dev.vote_count > 1:
                    response_data['error'] = 'Sorry, you already voted for 2 members'
                else:
                    if bem.vote != None:
                        vote = bem.vote

                        for user in vote.users.all():
                            if dev.name == user.name:
                                voted = True
                                response_data['error'] = 'Sorry, you already voted for this member'
                                break
                        if voted == False:
                            vote.users.add(dev)
                            vote.save()
                            dev.vote_count += 1
                            dev.save()
                            response_data['success'] = 'Success, your vote was submitted to server'
                    else:
                        vote = Vote()
                        vote.save()
                        vote.users.add(dev)
                        bem.vote = vote
                        bem.save()
                        dev.vote_count += 1
                        dev.save()
                        voted = True
                        response_data['success'] = 'Success, your vote is submit to server'

            except ObjectDoesNotExist:
                response_data['error'] = 'Sorry, you are not Windows user'
        else:
            response_data['error'] = 'Sorry, please login before voting'

        response_data['voted'] = voted
        return render(request, 'windows/bem.html', response_data)
    else:
        bems = bem = None
        voted = False
        if bem_id == 'all':
            bems = Bem.objects.all().order_by('-date')
        else:
            try:
                bem = Bem.objects.get(pk=bem_id)
                if not bem.vote is None:
                    if request.user.developer in bem.vote.users.all():
                        voted = True
            except ObjectDoesNotExist:
                bem = None
        return render(request, 'windows/bem.html', {'bems': bems, 'bem': bem, 'voted': voted})

@login_required()
def profile(request, dev_id):
    devs = Developer.objects.filter(user__username=dev_id)
    if devs.count() == 0:
        dev = None
    else:
        dev = devs[0]

    return render(request, "windows/profile.html", {'dev': dev})

@login_required
def activities(request):
    devs = Developer.objects.all()
    bems = Bem.objects.all().order_by('-date')
    activity = Activity.objects.all().order_by('-date')
    return render(request, 'windows/activities.html', {'devs': devs, 'bems': bems, 'activities': activity})

def announcement(request):
    announ = Announcement.objects.all().order_by('-date')
    return render(request, 'windows/announcement.html', {'announcements': announ})

def townhall(request):
    reset = False
    count = 1
    if request.method == 'POST':
        question_id = int(request.POST.get('comment_parent'))
        if question_id == 0:
            count = int(request.COOKIES.get('questions', '1'))
            if 'last_question' in request.COOKIES:
                last_question = request.COOKIES['last_question']
                last_question_time = datetime.strptime(last_question[:-7], "%Y-%m-%d %H:%M:%S")
                if (datetime.now() - last_question_time).days > 0:
                    count = 1
                    reset = True
                else:
                    count += 1
                    request.session['questions'] = count
            else:
                reset = True

            if count == 1:
                user = None
                if request.user.is_authenticated:
                    user = request.user
                question = Question(user=user)
                question.text = request.POST.get('comment')
                question.save()

        else:
            if request.user.is_authenticated:
                try:
                    question = Question.objects.get(pk=question_id)
                    reply = Reply(user=request.user, question=question)
                    reply.text = request.POST.get('comment')
                    reply.save()
                    question.save()
                except ObjectDoesNotExist:
                    pass
    l_count = models.Count('likes')
    questions = Question.objects.annotate(l_count=l_count).order_by('-l_count')
    response = render(request, "windows/townhall.html", {'questions': questions})
    if reset:
        response.set_cookie('last_question', datetime.now())
        response.set_cookie('questions', count)
    return response

def like(request):
    response = {}
    if request.method == 'POST':
        question_id = int(request.POST.get('id'))
        like = request.POST.get('like')

        if request.user.is_authenticated:
            user = request.user
            try:
                question = Question.objects.get(pk=question_id)
                if like == 'true':
                    if user not in question.likes.all():
                        question.likes.add(user)
                        question.save()
                    if user in question.dislikes.all():
                        question.dislikes.remove(user)
                        question.save()
                else:
                    if user in question.likes.all():
                        question.likes.remove(user)
                        question.save()
                    if user not in question.dislikes.all():
                        question.dislikes.add(user)
                        question.save()
            except ObjectDoesNotExist:
                pass

        response['likes'] = question.likes.all().count()
        response['dislikes'] = question.dislikes.all().count()
        return JsonResponse(response)

def userLogin(request):
    message = None
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        nextUrl = request.POST.get("next", "/")
        user = authenticate(username=username, password=password)
        message = "Sorry, wrong username or password."
        if user is not None:
            login(request, user)
            return redirect(nextUrl)
    else:
        if request.user.is_authenticated:
            return redirect('/')

    return render(request, 'windows/login.html', {'message': message})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
