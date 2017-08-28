from django.shortcuts import render, get_object_or_404
from .models import Question, Survey, Response, Answer
from .forms import SurveyForm, ResponseForm, QuestionForm
from .forms import QuestionFormSet
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
"""
def index(request):
    all_surveys = Survey.objects.all()
    return render(request, 'dyform/index.html',{'all_surveys':all_surveys})
"""
class SurveyList(ListView):
    model = Survey
class SurveyCreate(CreateView):
    model = Survey
    fields = ['title', 'desc']
class SurveyUpdate(UpdateView):
    model = Survey
    success_url = '/'
    fields = ['title', 'desc']
"""
def create_survey(request):
    created = False
    if request.method == 'POST':
        form = SurveyForm(data=request.POST)
        if form.is_valid():
            created = True
            survey = form.save(commit=False)
            survey.save()
            print("created",created)
            return render(request, 'dyform/create_survey.html', {'form': form, 'created': created, 'survey': survey})
        else:
            print(form.errors)
    else:
        form = SurveyForm()
    return render(request, 'dyform/create_survey.html', {'form': form, 'created': created})
"""
class SurveyQuestionCreate(CreateView):
    model = Survey
    fields = ['title', 'desc']
    #template_name = 'dyform/edit_survey.html'
    success_url = reverse_lazy('survey-list')
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
    success_url = reverse_lazy('survey-list')

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
"""
def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey,  pk=survey_id)
    print(survey)
    if request.method == 'POST':
        form = QuestionForm(survey=survey, data=request.POST, extra=request.POST.get('extra_question_count'))
        if form.is_valid():
            question_form = form.save(commit=False)
            question_form.save()
        else:
            print(form.errors)
    else:
        print("else............part") 
        form = QuestionForm(survey=survey)  
         
    return render(request, 'dyform/edit_survey.html', {'form': form, 'survey': survey})
"""