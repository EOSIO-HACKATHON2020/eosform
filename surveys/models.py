import json
import enum
import requests
from django.contrib.postgres.fields import ArrayField
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from config.models import Settings
from users.models import User
from . import utils


class SurveyStatus(enum.IntEnum):
    DRAFT = 1
    PUBLISHED = 2
    DELETED = 3

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
    uid = models.CharField(default=utils.gen_eos_username,
                           editable=False, unique=True, max_length=12,
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

    def get_absolute_url(self) -> str:
        return reverse('surveys:survey', args=(self.uid,))

    def get_publish_url(self) -> str:
        return reverse('surveys:action', args=(self.uid, 'publish'))

    def get_delete_url(self) -> str:
        return reverse('surveys:action', args=(self.uid, 'delete'))

    def get_responses_curl(self) -> str:
        """
        cURL link to retrieve data in JSON format
        :return: string
        """
        settings = Settings.get_solo()
        endpoint = f'{settings.eos_node_uri}/v1/chain/get_table_rows'
        data = json.dumps({
            'code': settings.eos_account,
            'table': 'response',
            'scope': self.uid,
            'limit': 10000,
            'json': True
        })
        return f'curl --request "POST" ' \
               f'--url {endpoint} ' \
               f'--data \'{data}\''

    def get_response_url(self):
        settings = Settings.get_solo()
        return f'{settings.domain}' \
               f'{reverse("surveys:response", args=(self.uid,))}'

    def get_json_url(self):
        return f'{reverse("surveys:json", args=(self.uid,))}'

    def get_origin(self):
        if self.id:
            return Survey.objects.filter(id=self.id).first()
        return None

    @property
    def is_draft(self) -> bool:
        return self.status == SurveyStatus.DRAFT.value

    @property
    def is_published(self) -> bool:
        return self.status == SurveyStatus.PUBLISHED.value

    @property
    def is_deleted(self) -> bool:
        return self.status == SurveyStatus.DELETED.value

    @property
    def is_publishing(self) -> bool:
        origin = self.get_origin()
        if origin and origin.is_draft and self.is_published:
            return True
        return False

    @property
    def is_deleting(self) -> bool:
        origin = self.get_origin()
        if origin and origin.is_published and self.is_deleted:
            return True
        return False

    def eos_publish(self) -> str:
        """
        Send the command to the EOSGate service and return trxid or error
        message
        :return:
        """
        config = Settings.get_solo()
        uri = f'{config.eosgate}/form'
        payload = {
            'form': self.uid,
            'questions': list(self.questions.values_list('name', flat=True))
        }
        r = requests.post(uri, json=payload)
        if r.status_code == 200:
            self.status = SurveyStatus.PUBLISHED.value
            self.save()
        return r.content.decode()

    def eos_delete(self) -> str:
        config = Settings.get_solo()
        uri = f'{config.eosgate}/form'
        payload = {
            'form': self.uid,
        }
        r = requests.delete(uri, json=payload)
        return r.content.decode()

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
                               null=True, blank=False,
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


class Participation(TimeStampedModel):
    """
    User that passed
    """
    user = models.ForeignKey('users.User', related_name='surveys_participated',
                             on_delete=models.CASCADE, null=True,
                             blank=True)
    survey = models.ForeignKey('surveys.Survey', related_name='users',
                               on_delete=models.CASCADE, null=True, blank=True)
    txid = models.CharField(_('Transaction ID'), max_length=64,
                            null=True, blank=True)

    class Meta:
        unique_together = ('user', 'survey')

    def get_testnet_url(self):
        return f'https://testnet.eos.io/transaction/{self.txid}'
