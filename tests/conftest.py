import pytest
from django.core.management import call_command


@pytest.fixture()
def load_fixtures():
    return _load_fixtures


def _load_fixtures(*fixtures):
    call_command('loaddata', *fixtures)
