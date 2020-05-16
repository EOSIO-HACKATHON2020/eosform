from django.contrib import admin
from .models import Survey
from .models import Question


class QuestionInline(admin.TabularInline):
    model = Question
    fields = [
        'name',
        'is_required',
        'type',
        'description',
    ]
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'uid',
        # 'status'
        'user',
        'modified',
        'created',
    ]
    list_filter = [
        'modified',
        'created',
    ]
    autocomplete_fields = [
        'user'
    ]
    search_fields = [
        'uid',
        'name',
        'user',
    ]
    readonly_fields = [
        'uid'
    ]
    inlines = [
        QuestionInline,
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'is_required',
        'type',
        'modified',
        'created',
    ]
    radio_fields = {
        'type': admin.VERTICAL
    }
    list_filter = [
        'type',
        'is_required',
        'modified',
        'created',
    ]
    autocomplete_fields = [
        'survey'
    ]
    search_fields = [
        'name',
    ]
