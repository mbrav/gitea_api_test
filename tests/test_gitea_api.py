
from urllib.parse import urljoin

import pytest
import requests
from gitea_api import __version__


def test_version():
    assert __version__ == '0.1.0', (
        'Bad version number'
    )


def test_env(get_env):
    print(get_env)
    assert get_env, (
        'Bad env config'
    )


def test_api_health(wait_for_api):
    """The Api is now verified good to go and tests can interact with it"""

    response = wait_for_api
    assert response.code == 200, (
        'Response code not 200'
    )


if __name__ == '__main__':
    pytest.main(['--docker-compose', './docker',
                 '--docker-compose-no-build'])
