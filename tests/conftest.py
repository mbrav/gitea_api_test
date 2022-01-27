import os

import pytest
from dotenv import load_dotenv
from gitea_api.main import GiteaAPI
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

pytest_plugins = ["docker_compose"]


@pytest.fixture(scope='session', autouse=True)
def get_env():
    env = {
        'ADMIN_USER': os.environ.get('ADMIN_USER'),
        'ADMIN_EMAIL': os.environ.get('ADMIN_EMAIL'),
        'ADMIN_PASSWORD': os.environ.get('ADMIN_PASSWORD'),
        'GITEA_PORT': os.environ.get('GITEA_PORT'),
    }
    return env


@pytest.fixture(scope='session')
def admin_session(get_env):
    admin_login = {
        'username': get_env['ADMIN_USER'],
        'password': get_env['ADMIN_PASSWORD'],
        'email': get_env['ADMIN_EMAIL'],
    }

    admin = GiteaAPI(**admin_login)
    return admin


@pytest.fixture(scope='session')
def user_session():
    user_login = {
        'username': 'test',
        'email': 'test@test.com',
        'password': 'test12',
    }
    user = GiteaAPI(**user_login)
    return user


@pytest.fixture(scope="function")
def wait_for_api(function_scoped_container_getter, get_env, admin_session):
    """Wait for the api from my_api_service to become responsive"""

    service = function_scoped_container_getter.get("server").network_info[0]

    admin_session.set_base_url(service.hostname, get_env['GITEA_PORT'])

    response = admin_session.health_check()
    return response
