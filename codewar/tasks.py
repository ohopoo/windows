# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from channels import Channel
import json
from codewar.models import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import subprocess
from subprocess import PIPE
from django.contrib.auth.models import User
from bem.settings import TEMPORARY
ROOT = TEMPORARY #'/Users/TuDinhTan/Desktop/Projects/CodeFights/temporary/'

def sendMessage(channel, message):
    # Send status update back to browser client
    if channel is not None:
        Channel(channel).send({
            "text": json.dumps(message)
        })
#   check answer for text question
def checkAnswer(question, user, input):
    exits = Answer.objects.filter(user=user).filter(question=question).filter(state=0).first()
    if not exits:
        if question and input:
            if question.testcase.first().input == input:
                message = "This answer is accepted !"
                ans = Answer(user=user, content=input, question=question, result='Accepted', state=0)
                ans.save()
                user, created = GLUser.objects.get_or_create(user=user)
                if created:
                    user.score = question.score
                else:
                    user.score = user.score + question.score
                user.save()
            else:
                message = "This answer is incorrect !"
        else:
            message = "Please input an answer !"
    else:
        message = "You already submit corrrected answer !"
    return message
#functions for code question
def compileSrc(src):
    file = default_storage.save(ROOT + "f.cpp" , ContentFile(src))
    compile = subprocess.Popen([r"/usr/bin/c++", "-Wall", "-o", file + ".out", file], stdout=PIPE,
                               stderr=PIPE)
    return (file, compile.communicate())

def runWithParam(appFile,param):
    appTest = subprocess.Popen([appFile + ".out"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    lines = b""
    for lineInput in str(param).splitlines():
        lines += bytes(lineInput + "\n", 'utf-8')
    print(lines)
    output = appTest.communicate(input=lines)[0]
    return output

@task
def genTestcase(id):
    print(id)
    question  = Question.objects.get(id=id)
    file, error = compileSrc(question.solution)
    print(error)
    print("---here--")
    if error ==(b'',b''):
        for testcase in question.testcase.all():
            print(testcase.input)
            result = runWithParam(file,testcase.input)
            testcase.output = result
            testcase.save()

@task(time_limit=5)
def compileAndTest(id, reply_channel, username, score):
    answer =  Answer.objects.get(id=id)
    # save file and compile
    file, answer.result = compileSrc(answer.content)
    if answer.result == (b'', b''):
        answer.state = 1  # compile successfully
        sendMessage(reply_channel, {'state':"Compiled", "message":"- Compile successfully"})
    else:
        answer.state = 2  # compile failed
        sendMessage(reply_channel, {'state':"Compile",
                                    "message":"- Compile error \n" +
                                    answer.result[1].decode("utf-8") })#.decode('ascii')).replace(ROOT,"")})
    answer.save()

    if answer.state == 1:
        # do testcase
        answer.result = "Accepted"
        answer.state = 0 #finished
        for index,testcase in enumerate(answer.question.testcase.all()):
            output = runWithParam(file, testcase.input)
            print(output)
            solution = bytes(testcase.output.replace('\r',''),'utf-8')
            print(solution)
            if output != solution: # 'A' ==b'A' false in python3
                answer.result = "Failed in test case: %s" % str(index + 1)
                answer.state = 3 # failed testcase
                answer.save()
                sendMessage(reply_channel, {'state':"Failed",'color':'red',"message":"3. "+answer.result})
                return
        answer.save()
        user = User.objects.get(username=username)
        glUser, created = GLUser.objects.get_or_create(user=user)
        if created:
            glUser.score = score
        else:
            glUser.score = glUser.score + score
        glUser.save()
        sendMessage(reply_channel, {'state': "Finished", "message": "- Answer accepted"})

def start_compile(username, data, reply_channel):
    print (data)
    user = User.objects.get(username=username)
    question = Question.objects.get(id=int(data['question_id']))
    if not question:
        sendMessage(reply_channel, {'state': "Error !",'color':'red', "message": "Questions not found"})
        return
    if not data['editor']:
        sendMessage(reply_channel, {'state': "Error !",'color':'red', "message": "Have you coded ?"})
        return
    if user:
        exits = Answer.objects.filter(user=user).filter(question=question).filter(state=0).first()
        if not exits:
            answer = Answer(user=user, content=data['editor'], question=question)
            answer.save()
            taskid = compileAndTest.delay(answer.id, reply_channel, username, question.score)
            answer.taskID = taskid
            answer.save()
            sendMessage(reply_channel, {'state': "Wait", "message": "- Your answer has sent to queue"})
        else:
            sendMessage(reply_channel, {'state': "Finished", "message": "- You already sovled it"})
    else:
        sendMessage(reply_channel, {'state': "Error !",'color':'red', "message": "You need to login first"})