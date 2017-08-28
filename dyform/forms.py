from django import forms
from django.forms import models
from django.core.urlresolvers import reverse
from django.dispatch import Signal
from django.shortcuts import get_object_or_404
from .models import Survey, Question, Response, Answer
from django.forms import inlineformset_factory
class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'desc']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ()
        
QuestionFormSet = inlineformset_factory(Survey, Question, form=QuestionForm, extra=1)
# scratch implementation **not working
"""
class QuestionForm(forms.ModelForm):
    extra_question_count = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Question
        fields = ('title', )
    def __init__(self, survey=None, *args, **kwargs):
        self.survey = survey
        extra_questions = kwargs.pop('extra', 0)
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['extra_question_count'].initial = extra_questions
        for idx in range(int(extra_questions)):
            self.fields['extra_question_%d' %idx] = forms.CharField()
    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)
        question.survey = self.survey
        question.save()
        data = {
            'survey_id': question.survey.id,    
            'questions': []
        }
        print(self.cleaned_data)
        for field_name, field_value in enumerate(self.cleaned_data):
            #if field_name.startswith('extra_question_'):
            q = Question()
            q.title = field_value
            q.survey = self.survey
            q.save()
            data['questions'].append((q.id, q.title))
        #calling db_signal
        Signal(providing_args=["instance", "data"]).send(sender=Question, instance=question, data=data)
        return question
"""
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ()
    def __init__(self, *args, **kwargs):
        survey = kwargs.pop('survey')
        #https://jacobian.org/writing/dynamic-form-generation/
        self.survey = survey
        super(ResponseForm, self).__init__(*args, **kwargs)
        data = kwargs.get('data')
        for idx, q in enumerate(survey.questions()):
            print(idx, q)
            self.fields['question_%d' %q.pk] = forms.CharField(label=q.title,
                widget=forms.Textarea)
            if data:
                self.fields['question_%d' %q.pk].initial = data.get('question_%d'%q.pk)
    def save(self, commit=True):
        response = super(ResponseForm, self).save(commit=False)
        response.survey = self.survey
        response.save()
        data = {
            'survey_id': response.survey.id,    
            'responses': []
        }
        for field_name, field_value in self.cleaned_data.iteritems():
            if field_name.startswith('question_'):
                q_id = int(field_name.split('_')[1])
                q = Question.objects.get(pk=q_id)
                ans = Answer(question=q)
                ans.text = field_value
            data['responses'].append((ans.question.id, ans.text))
            ans.response = response
            ans.save()
        #calling db_signal
        Signal(providing_args=["instance", "data"]).send(sender=Response, instance=response, data=data)
        return response