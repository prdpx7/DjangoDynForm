from django.conf.urls import url
from . import views
app_name = 'dyform'

urlpatterns = [
    url(r'^$', views.SurveyList.as_view(), name='survey-list'),
    url(r'survey/create/$', views.SurveyQuestionCreate.as_view(), name='survey-create'),
    url(r'survey/update/(?P<pk>[0-9]+)/$', views.SurveyQuestionUpdate.as_view(), name='survey-update'),
    url(r'survey/(?P<id>[0-9]+)/$', views.survey_response, name='survey_response')
]