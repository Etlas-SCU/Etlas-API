from django.contrib import admin
from .models import Choice, Question

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('statement', 'label', 'correct_chocie')
    filter_horizontal = ('choices',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
