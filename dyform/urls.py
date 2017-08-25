from django.conf.urls import url
from . import views
app_name = 'dyform'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create_survey, name='create_survey'),
    url(r'^edit/(?P<survey_id>[0-9]+)/$', views.edit_survey, name='edit_survey'),
]