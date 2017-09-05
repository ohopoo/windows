from django.contrib import admin
from codewar.models import *
from codewar.tasks import genTestcase
# Register your models here.
class GLUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'score', 'avatar']

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 0

def createTestCase(modeladmin, request, queryset):
    for obj in queryset:
        if obj.type ==0: #code
            genTestcase.delay(obj.id)

createTestCase.short_description = "Create TestCases for selected questions"

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title','type','score','published','created','modified']
    list_filter = ['type']
    search_fields = ['title','content']
    inlines = [AttachmentInline, TestCaseInline]
    actions = [createTestCase]

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['question', 'file']

class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['question', 'input', 'output']
    search_fields = ['input', 'output']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user','question','language', 'state']
    list_filter = ['language','state']
    search_fields = ['content']

admin.site.register(GLUser, GLUserAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(Answer, AnswerAdmin)