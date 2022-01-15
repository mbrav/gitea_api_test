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
        return r.status

    @staticmethod
    def create_user(username: str, email: str, password: str):
        r = http.request('GET', BASE_URL)
        assert r.status == 201

    def _get_headers(self):
        """Генерируем хедары на основе наличия токена"""

        if self.token:
            print('GOT TOKEN')
            headers = {
                'Authorization': f'token {self.token}',
                'Content-Type': 'application/json'
            }
            return headers

        headers = urllib3.make_headers(
            basic_auth=f'{self.username}:{self.password}')
        return headers

    def create_user(self, username: str, email: str, password: str):
        """Создаём пользователя"""

        data = json.dumps({
            'email': email,
            'password': password,
            'username': username,
            'full_name': username,
            'must_change_password': False,
        })

        headers = self._get_headers()

        url = f'{BASE_URL}/api/v1/admin/users'

        r = http.request('POST', url, body=data, headers=headers)

        r_data = json.loads(r.data.decode('utf-8'))

        # assert r.status == 201
        return r.status, r_data

    def get_users(self):
        """Получаем список пользователей"""

        headers = self._get_headers()

        url = f'{BASE_URL}/api/v1/admin/users'
        r = http.request('GET', url, headers=headers)

        r_data = json.loads(r.data.decode('utf-8'))

        assert r.status == 200
        return r.status, r_data

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

        print(f'Token {self.token}')
        assert r.status == 201
        return r.status, r_data

    def get_repositories(self):
        """Получаем список репозиторий"""

        headers = self._get_headers()

        url = f'{BASE_URL}/api/v1/user/repos'
        r = http.request('GET', url, headers=headers)

        r_data = json.loads(r.data.decode('utf-8'))

        assert r.status == 200
        return r.status, r_data

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
        return r.status, r_data

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
        return r.status, r_data

    def get_file_from_repository(self,
                                 repo: str,
                                 filepath: str):
        """Получаем фаил из репозитории"""

        headers = self._get_headers()

        url = f'{BASE_URL}/api/v1/repos/{self.username}/{repo}/contents/{filepath}'
        r = http.request('GET', url, headers=headers)

        r_data = json.loads(r.data.decode('utf-8'))

        assert r.status == 200
        return r.status, r_data


if __name__ == '__main__':
    GiteaAPI.health_check()

    admin_login = {
        'username': 'gitadmin',
        'email': 'admin@example.com',
        'password': 'password',
        'token': '070008382fdf2f57ab694b031eea9e61e13f8b30',
    }

    user_login = {
        'username': 'test',
        'email': 'test@test.com',
        'password': 'test12',
        # 'token': 'be52619ae267b8393b53b1287a73ad50861f7599',
    }

    admin = GiteaAPI(**admin_login)
    # admin.create_token()
    print(admin.create_user(**user_login))
    print(admin.get_users())

    user = GiteaAPI(**user_login)
    user.create_token()
    user.get_repositories()
    user.create_repository(name='test_repo')
    user.add_file_to_repository(repo='test_repo', filepath='main.py')
    user.get_file_from_repository(repo='test_repo', filepath='main.py')
