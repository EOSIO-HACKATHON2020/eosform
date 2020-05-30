from django.contrib import admin
from django.utils.translation import gettext as _
from .models import Survey
from .models import Question
from .models import Participation


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


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = [
        'txid',
        'survey_name',
        'user',
        'modified',
        'created',
    ]
    list_filter = [
        'created',
        'modified',
    ]
    search_fields = [
        'txid',
        'survey__uid',
        'survey__name',
    ]

    def survey_name(self, obj):
        return obj.survey.uid

    survey_name.short_description = _('Survey UID')

