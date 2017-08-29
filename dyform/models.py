from django.db import models
from django.core.urlresolvers import reverse
class Survey(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk)
        else:
            return Question.objects.none()
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('survey-update', kwargs={'pk': self.pk})
    
class Question(models.Model):
    survey = models.ForeignKey(Survey)
    title = models.CharField(max_length=200, blank=False, null=False)
    def __str__(self):
        return self.title 

class Response(models.Model):
    survey = models.ForeignKey(Survey)
    def __str__(self):
        return "Responses from " + self.survey.title
    

class Answer(models.Model):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response)
    text = models.TextField(blank=False, null=False)
    def __str__(self):
        return self.question.title + "|" + self.text

