from django.conf.urls import url
from . import views
app_name = 'dyform'

urlpatterns = [
    url(r'^$', views.SurveyList.as_view(), name='survey-list'),
    #url(r'^create/$', views.create_survey, name='create_survey'),
    url(r'survey/add/$', views.SurveyQuestionCreate.as_view(), name='survey-create'),
    url(r'survey/(?P<pk>[0-9]+)/$', views.SurveyQuestionUpdate.as_view(), name='survey-update'),
]