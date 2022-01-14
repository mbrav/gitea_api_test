import json
import pprint

import urllib3

http = urllib3.PoolManager()
pp = pprint.PrettyPrinter(indent=1)

BASE_URL = 'http://localhost:3000'


class GiteaAPI:
    """Класс GiteaUser"""

    def __init__(
            self, username: str, email: str, password: str, token: str = None):
        self.username = username
        self.email = email
        self.password = password
        self.token = token

    def get_headers(self):
        """Генерируем хедары на основе наличия токена"""

        if self.token:
            headers = {
                'Authorization': f'token {self.token}'
            }
            return headers
        headers = urllib3.make_headers(
            basic_auth=f'{self.username}:{self.password}')
        return headers

    def create_user(self):
        """Создаём пользователя"""

        data = {
            'email': self.email,
            'password': self.password,
            'username': self.username,
        }
        # user = NewUser(**data)
        r = http.request('POST', BASE_URL)

    def create_token(self):
        """Создаём токен"""

        data = {
            'name': self.username,
        }

        headers = self.get_headers()

        url = f'{BASE_URL}/api/v1/users/{self.username}/tokens'

        r = http.request('POST', url, fields=data, headers=headers)

        assert r.status == 201

        r_data = json.loads(r.data.decode('utf-8'))
        self.token = r_data.get('sha1')
        print(f'Token {self.token}')

    def get_repositories(self):
        """Получаем список репозиторий"""

        headers = self.get_headers()

        url = f'{BASE_URL}/api/v1/user/repos'
        r = http.request('GET', url, headers=headers)
        assert r.status == 200

        r_data = json.loads(r.data.decode('utf-8'))

        pp.pprint(r_data)

    def create_repository(self, name: str = 'test_repo',
                          description: str = 'Test Repository'):
        """Создаём новый репозитории"""

        data = {
            'auto_init': True,
            'default_branch': 'master',
            'description': description,
            'gitignores': 'Python',
            'license': 'MIT',
            'name': name,
            'private': False,
            'template': True,
            'trust_model': 'default'
        }

        headers = self.get_headers()

        url = f'{BASE_URL}/api/v1/user/repos'
        r = http.request('POST', url, fields=data, headers=headers)
        assert r.status == 201

        r_data = json.loads(r.data.decode('utf-8'))
        pp.pprint(r_data)

    def add_file_to_repository(self,
                               repo: str,
                               filepath: str):
        """Создаём новый фаил в репозитории"""

        data = {
            'author': {
                'email': self.email,
                'name': self.username
            },
            'committer': {
                'email': self.email,
                'name': self.username
            },
            'content': b'ZGVmIHRlc3QoKToKICAgIHByaW50KCd0ZXN0JykK',
            'message': f'Add {filepath}',
        }

        headers = self.get_headers()

        url = f'{BASE_URL}/api/v1/repos/{self.username}/{repo}/contents/{filepath}'
        r = http.request('POST', url, fields=data, headers=headers)
        # assert r.status == 201

        r_data = json.loads(r.data.decode('utf-8'))
        pp.pprint(r_data)

    def get_file_from_repository(self,
                                 repo: str,
                                 filepath: str):
        """Получаем фаил из репозитории"""

        headers = self.get_headers()

        url = f'{BASE_URL}/api/v1/repos/{self.username}/{repo}/contents/{filepath}'
        r = http.request('GET', url, headers=headers)
        assert r.status == 200

        r_data = json.loads(r.data.decode('utf-8'))
        pp.pprint(r_data)


if __name__ == '__main__':
    r = http.request('GET', BASE_URL)
    assert r.status == 200

    data = {
        'username': 'test',
        'email': 'test@test.com',
        'password': 'test12',
        'token': '9b329b9aaf76f6a469618a8a5ce9e3a577a33c0e',
    }

    user = GiteaAPI(**data)
    # user.get_repositories()
    # user.create_repository(name='test_repo')
    user.add_file_to_repository(repo='test_repo', filepath='main.py')
    # user.get_file_from_repository(repo='test_repo', filepath='README.md')
