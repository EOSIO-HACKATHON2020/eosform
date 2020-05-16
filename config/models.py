from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class Settings(SingletonModel):
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return _('Settings')

    class Meta:
        verbose_name = _('Settings')
