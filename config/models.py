from django.db import models
from django.utils.translation import gettext as _
from solo.models import SingletonModel


class Settings(SingletonModel):
    maintenance_mode = models.BooleanField(default=False)
    domain = models.URLField(_('Site Domain'), blank=True, null=True,
                             help_text=_('e.g. https://beta.eosform.app'))
    eosgate = models.URLField(_('EOSGate URI'), blank=True, null=True,
                              help_text=_('e.g. http://localhost:8080'))
    eos_account = models.CharField(_('EOS Account'), max_length=12, null=True,
                                   blank=True)
    eos_node_uri = models.URLField(
        _('EOS Node URI'), blank=True, null=True,
        help_text=_('e.g. https://api.testnet.eos.io'))

    def __str__(self):
        return _('Settings')

    class Meta:
        verbose_name = _('Settings')
