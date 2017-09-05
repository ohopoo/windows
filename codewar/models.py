from django.db import models
from django.contrib.auth.models import User
import random
import string
from tinymce.models import HTMLField


def randomString():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

def user_directory_path(instance, filename):
    if hasattr(instance,'user'):
        return '{0}/{1}_{2}'.format(instance.user.username,randomString(), filename)
    return '{0}_{1}'.format(randomString(),filename)

class GLUser(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gluser')
    avatar      = models.ImageField(upload_to=user_directory_path, default=None, blank=True)
    score       = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class Question(models.Model):
    TYPE  = ((0,'Code'),
             (1,'Text'))
    # user                = models.ForeignKey(User, related_name="question")
    type                = models.IntegerField(choices=TYPE, default=0)
    title               = models.CharField(max_length=255)
    score               = models.IntegerField(default=0)
    content             = HTMLField()
    solution            = models.TextField(null=True, blank=True)
    created             = models.DateTimeField(auto_now_add=True)
    modified            = models.DateTimeField(auto_now=True)
    published           = models.BooleanField(default=False)
    def testCaseCount(self):
        return self.testcase.count()
    def list_sovled(self):
        return Answer.objects.filter(question=self).filter(state=0)
    def __str__(self):
        return self.title

class Attachment(models.Model):
    question            = models.ForeignKey(Question, related_name='attachment')
    file                = models.FileField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.file

class TestCase(models.Model):
    question            = models.ForeignKey(Question, related_name='testcase')
    input               = models.TextField(null=True, blank=True)
    output              = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.input[:80]

class Answer(models.Model):
    LANG                =   ((".c",'C'),
                            (".cpp", 'C++'),
                            (".java", 'Java'),
                            (".py", 'Python'))

    STATE               =   ((0, 'Finished'),
                            (1, 'Compile successfully'),
                            (2, 'Compile Failed'),
                            (3, 'TestCase Failed'))

    user                = models.ForeignKey(User, related_name="answer")
    question            = models.ForeignKey(Question, related_name='answer')
    content             = models.TextField()
    language            = models.CharField(max_length=5,choices=LANG,default='.cpp', null=True, blank=True)
    taskID              = models.CharField(max_length=126, null=True, blank=True)
    state               = models.IntegerField(choices=STATE, null=True, blank=True)
    result              = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content[:80]