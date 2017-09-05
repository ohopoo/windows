from django.conf.urls import include, url
# from django.contrib import admin
# admin.autodiscover()
from codewar.views import *
urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^editor/(?P<question_id>\d+)$', codeEditor, name="editor"),
    url(r'^profile/(?P<username>\S+)$', profile, name="profile"),
    # url(r'^login$', user_login, name="login"),
    # url(r'^logout', user_logout, name="logout"),
    # url(r'^account$', account, name="account"),
]
