from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

ALLOWED_HOSTS = [
    'www.eosform.app',
    'eosform.app',
]

sentry_sdk.init(
    dsn=env.str('SENTRY_DSN'),
    environment=env.str('SENTRY_ENVIRONMENT'),
    release=env.str('SENTRY_RELEASE'),
    integrations=[DjangoIntegration()],
    send_default_pii=True
)

INSTALLED_APPS += (
    'anymail',
)

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

ANYMAIL = {
    "MAILGUN_API_KEY": env.str('MAILGUN_API_KEY'),
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
}
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
