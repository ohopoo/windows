from django.conf.urls import url
from windows import views

app_name = 'windows'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^activities/$', views.activities, name='activities'),
    url(r'^announcement/$', views.announcement, name='announcement'),
    url(r'^townhall/$', views.townhall, name='townhall'),
    url(r'^like/$', views.like, name='like'),
    url(r'^report/$', views.report, name='report'),
    url(r'^sendreport/$', views.sendreport, name='sendreport'),
    url(r'^team/(?P<team_id>[\w.]+)/$', views.team, name='team'),
    url(r'^bem/(?P<bem_id>[\w.]+)/$', views.bem, name='bem'),
    url(r'^quiz/$', views.quiz, name='quiz'),
    url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
    url(r'^profile/(?P<dev_id>[\w.]+)/$', views.profile, name='profile'),
]