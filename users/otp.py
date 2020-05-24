import logging
import uuid
from django.core.cache import cache
from django.conf import settings


logger = logging.getLogger(__name__)


class OTP:
    """
    Generate OTP code and store it into the cache storage
    """
    def __init__(self, otp_type: str, user_id: int):
        self.otp_type = otp_type
        self.user_id = user_id
        self.key = f'otp_{otp_type}_{user_id}'
        self.code = self.get_code()

    @staticmethod
    def get_timeout():
        return settings.OTP_EXPIRY

    def set_code(self):
        code = f'{uuid.uuid4()}'
        cache.set(self.key, code, timeout=self.get_timeout())
        logger.info(f'Generated OTP code for {self.user_id}')
        return code

    def get_code(self):
        try:
            code = cache.get(self.key) or self.set_code()
        except Exception as e:
            logger.error(e)
        return code

    def __str__(self):
        return f'<OTP: {self.user_id}> {self.code}'

    def __repr__(self):
        return self.__str__()