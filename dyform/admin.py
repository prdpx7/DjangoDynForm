from django.contrib import admin
from .models import Question, Response, Survey, Answer
# Register your models here.
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
class AnswerInline(admin.StackedInline):
    model = Answer
    fields = ('question', 'text')
    readonly_fields = ('question',)
    extra = 0
class SurveyAdmin(admin.ModelAdmin):
    class Meta:
        model = Survey
    list_display = ('title',)
    inlines = [
        QuestionInline
    ]

class ResponseAdmin(admin.ModelAdmin):
    class Meta:
        model = Response
    list_display = ('survey',)
    inlines = [
        AnswerInline
    ]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
