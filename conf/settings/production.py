from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=env.str('SENTRY_DSN'),
    environment=env.str('SENTRY_ENVIRONMENT'),
    release=env.str('SENTRY_RELEASE'),
    integrations=[DjangoIntegration()],
    send_default_pii=True
)

INSTALLED_APPS += (

)
