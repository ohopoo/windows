# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'vote_count', 'vote_team', 'scores', 'city', 'level', 'phone', 'skype', 'birth', 'start']
    list_filter = ['team', 'level', 'city']

    search_fields = ['name']

class BemAdmin(admin.ModelAdmin):
    list_display = ['dev', 'score', 'is_best', 'expired', 'date', 'vote']
    search_fields = ['dev__name']

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', '__likes__', 'date']
    list_filter = ['user']

    inlines = [ReplyInline]

class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'general', 'achievement', 'plan', 'trouble', 'week']
    list_filter = ['name']
    ordering = ['name', 'week']

class QuizAdmin(admin.ModelAdmin):
    list_display = ['question', 'coding', 'level', 'answer']

admin.site.register(Team)
admin.site.register(Level)
admin.site.register(Activity)
admin.site.register(Achievement)
admin.site.register(Announcement)
admin.site.register(Link)
admin.site.register(Vote)
admin.site.register(Bem, BemAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Developer, UserAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Quiz, QuizAdmin)