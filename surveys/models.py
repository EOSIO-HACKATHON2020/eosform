import uuid
import enum
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.db import models
from users.models import User


class SurveyStatus(enum.IntEnum):
    DRAFT = 1
    PUBLISHED = 2
    DEACTIVATED = 3

    @classmethod
    def choices(cls):
        return [(tag.value, _(tag.name)) for tag in cls]


class Survey(TimeStampedModel):
    """
    Survey structure is defined here
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             related_name='surveys', null=False, blank=False,
                             verbose_name=_('User'),
                             help_text=_('Survey owner'))
    name = models.CharField(_('Name'), max_length=255, null=False, blank=True,
                            default='')
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
                           null=False, blank=False, db_index=True,
                           help_text=_('UID will be used during EOS upload'))
    status = models.PositiveSmallIntegerField(
        _('Status'), null=False, blank=False, default=SurveyStatus.DRAFT.value,
        choices=SurveyStatus.choices()
    )

    def __str__(self):
        if self.name:
            return self.name
        return f'{self.uid}'

    class Meta:
        db_table = 'surveys'


class QuestionType(enum.IntEnum):
    EMAIL = 1
    PHONE = 2
    SHORT_TEXT = 3
    LONG_TEXT = 4
    NUMBER = 5
    OPTIONS = 6
    CHECKBOXES = 7

    @classmethod
    def choices(cls):
        return [(tag.value, _(tag.name)) for tag in cls]


class Question(TimeStampedModel):
    """
    Surveys will consist of questions
    """
    survey = models.ForeignKey('surveys.Survey', on_delete=models.CASCADE,
                               null=False, blank=False,
                               related_name='questions',
                               verbose_name=_('Question'))
    name = models.TextField(_('Name'), null=False, blank=False)
    description = models.TextField(_('Description'), null=True, blank=True,
                                   help_text=_('question\'s help text'))
    type = models.PositiveSmallIntegerField(
        _('Question Type'), choices=QuestionType.choices(),
        default=QuestionType.SHORT_TEXT.value, null=False, blank=False
    )
    is_required = models.BooleanField(
        _('Is required?'), default=True,
        help_text=_('Question must be answered in order to submit response'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'questions'
