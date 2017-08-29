from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Question, Survey, Response, Answer
from .forms import SurveyForm, ResponseForm, QuestionForm
from .forms import QuestionFormSet
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.core.urlresolvers import reverse_lazy
from django.db import transaction

class SurveyList(ListView):
    model = Survey

class SurveyCreate(CreateView):
    model = Survey
    fields = ['title', 'desc']

class SurveyUpdate(UpdateView):
    model = Survey
    success_url = '/'
    fields = ['title', 'desc']

class SurveyQuestionCreate(CreateView):
    model = Survey
    fields = ['title', 'desc']
    #template_name = 'dyform/edit_survey.html'
    success_url = reverse_lazy('dyform:survey-list')
    def get_context_data(self, *args, **kwargs):
        print("buggggggggggg")
        print(self.__dict__)
        data = super(SurveyQuestionCreate, self).get_context_data(*args,**kwargs)

        if self.request.POST:
            data['questions'] = QuestionFormSet(self.request.POST)
        else:
            data['questions'] = QuestionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        questions = context['questions']
        with transaction.atomic():
            self.object = form.save()
            if questions.is_valid():
                questions.instance = self.object
                questions.save()
        return super(SurveyQuestionCreate, self).form_valid(form)


class SurveyQuestionUpdate(UpdateView):
    model = Survey
    fields = ['title', 'desc']
    success_url = reverse_lazy('dyform:survey-list')

    def get_context_data(self, **kwargs):
        data = super(SurveyQuestionUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = QuestionFormSet(self.request.POST, instance=self.object)
        else:
            data['questions'] = QuestionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        questions = context['questions']
        with transaction.atomic():
            self.object = form.save()
            if questions.is_valid():
                questions.instance = self.object
                questions.save()
        return super(SurveyQuestionUpdate, self).form_valid(form)

def survey_response(request, pk):
    survey = Survey.objects.get(pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save()
            return HttpResponse("Thank you for the submission")
    else:
        form = ResponseForm(survey=survey)
        print (form)
    return render(request, 'dyform/survey_response.html', {'response_form': form, 'survey':survey})
    