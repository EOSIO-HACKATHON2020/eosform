from django.db import models
from django.utils.translation import gettext as _
from solo.models import SingletonModel


class Settings(SingletonModel):
    maintenance_mode = models.BooleanField(default=False)
    domain = models.URLField(_('Site Domain'), blank=True, null=True,
                             help_text=_('e.g. https://beta.eosform.app'))

    def __str__(self):
        return _('Settings')

    class Meta:
        verbose_name = _('Settings')
