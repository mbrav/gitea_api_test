import json

import urllib3

http = urllib3.PoolManager()

BASE_URL = 'http://localhost:3000'


class GiteaAPI:
    """Класс GiteaUser"""

    def __init__(
            self, username: str, email: str, password: str, token: str = None):
        self.username = username
        self.email = email
        self.password = password
        self.token = token

    @staticmethod
    def health_check():
        r = http.request('GET', BASE_URL)
        assert r.status == 200

    def _get_headers(self):
        """Генерируем хедары на основе наличия токена"""

        if self.token:
            headers = {
                'Authorization': f'token {self.token}',
                'Content-Type': 'application/json'
            }
            return headers
        headers = urllib3.make_headers(
            basic_auth=f'{self.username}:{self.password}')
        return headers

    def create_user(self):
        """Создаём пользователя"""

        data = json.dumps({
            'email': self.email,
            'password': self.password,
            'username': self.username,
        })
        # user = NewUser(**data)
        r = http.request('POST', BASE_URL)

    def create_token(self):
        """Создаём токен"""

        data = {
            'name': self.username,
        }

        headers = self._get_headers()

        url = f'{BASE_URL}/api/v1/users/{self.username}/tokens'

        r = http.request('POST', url, fields=data, headers=headers)

        r_data = json.loads(r.data.decode('utf-8'))
        self.token = r_data.get('sha1')

        assert r.status == 201
        return r.status, r.data

    def get_repositories(self):
        """Получаем список репозиторий"""

        headers = self._get_headers()

        url = f'{BASE_URL}/api/v1/user/repos'
        r = http.request('GET', url, headers=headers)

        r_data = json.loads(r.data.decode('utf-8'))

        assert r.status == 200
        return r.status, r.data

    def create_repository(self, name: str = 'test_repo',
                          description: str = 'Test Repository'):
        """Создаём новый репозитории"""

        data = json.dumps({
            'auto_init': True,
            'default_branch': 'master',
            'description': description,
            'gitignores': 'Python',
            'license': 'MIT',
            'name': name,
            'private': False,
            'template': True,
            'trust_model': 'default'
        })

        headers = self._get_headers()

        url = f'{BASE_URL}/api/v1/user/repos'
        r = http.request('POST', url, body=data, headers=headers)

        r_data = json.loads(r.data.decode('utf-8'))

        assert r.status == 201
        return r.status, r.data

    def add_file_to_repository(self,
                               repo: str,
                               filepath: str):
        """Создаём новый фаил в репозитории"""

        data = json.dumps({
            'author': {
                'email': self.email,
                'name': self.username
            },
            'committer': {
                'email': self.email,
                'name': self.username
            },
            'content': 'ZGVmIHRlc3QoKToKICAgIHByaW50KCd0ZXN0JykK',
            'message': f'Add {filepath}',
        })

        headers = self._get_headers()

        url = f'{BASE_URL}/api/v1/repos/{self.username}/{repo}/contents/{filepath}'
        r = http.request('POST', url, body=data, headers=headers)

        r_data = json.loads(r.data.decode('utf-8'))

        assert r.status == 201
        return r.status, r.data

    def get_file_from_repository(self,
                                 repo: str,
                                 filepath: str):
        """Получаем фаил из репозитории"""

        headers = self._get_headers()

        url = f'{BASE_URL}/api/v1/repos/{self.username}/{repo}/contents/{filepath}'
        r = http.request('GET', url, headers=headers)

        r_data = json.loads(r.data.decode('utf-8'))

        assert r.status == 200
        return r.status, r.data


if __name__ == '__main__':
    GiteaAPI.health_check()

    data = {
        'username': 'test',
        'email': 'test@test.com',
        'password': 'test12',
        # 'token': '3a66b345916f911756bae5da1158bbc2169c4422',
    }

    user = GiteaAPI(**data)
    user.create_token()
    user.get_repositories()
    user.create_repository(name='test_repo')
    user.add_file_to_repository(repo='test_repo', filepath='main.py')
    user.get_file_from_repository(repo='test_repo', filepath='main.py')
