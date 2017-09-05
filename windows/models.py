# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

import calendar
from datetime import date

def user_directory_path(instance, filename):
    return 'profile/{0}/{1}'.format(instance.user.username, filename)

class Report(models.Model):
    name = models.CharField(max_length=128, blank=True)
    general = models.TextField(max_length=500, blank=True)
    achievement = models.TextField(max_length=500, blank=True)
    plan = models.TextField(max_length=500, blank=True)
    trouble = models.TextField(max_length=500, blank=True)
    week = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return ', '.join([self.general, self.achievement, self.plan, self.trouble])

class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)

    def __unicode__(self):
        return self.name

class Level(models.Model):
    level = models.CharField(max_length=50)

    def __unicode__(self):
        return self.level

class Quiz(models.Model):
    question = models.TextField(blank=True)
    coding = models.TextField(blank=True)
    answer = models.TextField(blank=True)
    description = models.TextField(blank=True)
    level = models.IntegerField(default=1)

    def __unicode__(self):
        return self.question + ' ' + self.answer

class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reports = models.ManyToManyField(Report, default=None, blank=True)
    quiz = models.ManyToManyField(Quiz, default=None, blank=True)
    scores = models.IntegerField(default=0, blank=True)
    team = models.ForeignKey(Team)
    level = models.ForeignKey(Level)
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    skype = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    start = models.DateField(blank=True)
    birth = models.DateField(blank=True)
    vote_count = models.IntegerField(default=0, blank=True)
    vote_team = models.BooleanField(default=False, blank=True)
    # image = models.FileField(upload_to=user_directory_path, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def birthday_party(self):
        return date.today().month == self.birth.month

class Vote(models.Model):
    users = models.ManyToManyField(Developer, default=None, blank=True)

    def __unicode__(self):
        return ', '.join([user.name for user in self.users.all()])

class Link(models.Model):
    title = models.CharField(max_length=128)
    link = models.URLField()

    def __unicode__(self):
        return self.title

class Bem(models.Model):
    dev = models.ForeignKey(Developer, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    ownership_responsibility = models.TextField(blank=True)
    technical_skills = models.TextField(blank=True)
    transparency_support = models.TextField(blank=True)
    confluence_link = models.ManyToManyField(Link, default=None, blank=True)
    vote = models.OneToOneField(Vote, default=None, blank=True, null=True)
    score = models.FloatField(default=0.0)
    is_best = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.dev.name

    def month_name(self):
        return calendar.month_name[self.date.month]

class Activity(models.Model):
    dev = models.ForeignKey(Developer)
    description = models.CharField(max_length=250, blank=True)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.dev.name + ' ' + self.description

class Achievement(models.Model):
    dev = models.ForeignKey(Developer)
    name = models.CharField(max_length=250, blank=True)
    link = models.URLField()
    date = models.DateTimeField()

    def __unicode__(self):
        return self.dev.name + ' ' + self.name

class Announcement(models.Model):
    author = models.ForeignKey(Developer)
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.author.name + ' ' + self.title

class Question(models.Model):
    user = models.ForeignKey(User, null=True)
    text = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, default=None, blank=True, related_name='dislikes')

    def __unicode__(self):
        return self.text

    def __likes__(self):
        return self.likes.all().count() - self.dislikes.all().count()

    @property
    def get_replies(self):
        return self.reply_set.order_by('-date')

class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text
