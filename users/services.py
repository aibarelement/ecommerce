import random
import uuid
from typing import Protocol, OrderedDict

from django.core.cache import cache
from rest_framework_simplejwt import tokens

from . import repos, models


class UserServicesInterface(Protocol):

    def create_user(self, data: OrderedDict) -> dict: ...

    def verify_user(self, data: OrderedDict) -> models.CustomUser | None: ...

    def create_token(self, data: OrderedDict) -> dict: ...


class UserServicesV1:
    user_repos: repos.UserReposInterface = repos.UserReposV1()

    def create_user(self, data: OrderedDict) -> dict:
        numbers = [str(i) for i in range(10)]
        code = ''.join(random.choices(numbers, k=4))
        session_id = str(uuid.uuid4())
        session = {'code': code, **data}
        cache.set(session_id, session, timeout=300)
        self._send_sms_to_phone_number(phone_number=data['phone_number'], code=code)

        return {
            'session_id': session_id,
        }

    def verify_user(self, data: OrderedDict) -> models.CustomUser | None:
        user_data = cache.get(data['session_id'])

        if not user_data:
            return

        if data['code'] != user_data['code']:
            return

        user = self.user_repos.create_user(data={
            'email': user_data['email'],
            'phone_number': user_data['phone_number'],
        })
        self._send_letter_to_email(email=user.email)

    @staticmethod
    def _send_letter_to_email(email: str) -> None:
        print(f'send letter to {email}')

    @staticmethod
    def _send_sms_to_phone_number(phone_number: str, code: str) -> None:
        print(f'send sms code {code} to {phone_number}')

    def create_token(self, data: OrderedDict) -> dict:
        user = self.user_repos.get_user(data=data)

        access = tokens.AccessToken.for_user(user=user)
        refresh = tokens.RefreshToken.for_user(user=user)

        return {
            'access': str(access),
            'refresh': str(refresh),
        }
