import json

import urllib3

http = urllib3.PoolManager()

BASE_URL = 'http://localhost:3000'


class GiteaUser:
    def __init__(self, username: str, password: str, token: str = None):
        self.username = username
        self.password = password
        self.token = token

    def get_headers(self):
        if self.token:
            headers = {
                'Authorization': f'token {self.token}'
            }
            return headers
        headers = urllib3.make_headers(
            basic_auth=f'{self.username}:{self.password}')
        return headers

    def create_token(self):
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

        headers = self.get_headers()

        url = f'{BASE_URL}/api/v1/user/repos'
        r = http.request('GET', url, headers=headers)

        assert r.status == 200

        r_data = json.loads(r.data.decode('utf-8'))

        print(r_data)

    def create_repository(self, name: str = 'test_repo'):
        data = {
            'name': name,
        }

        headers = self.get_headers()

        url = f'{BASE_URL}/api/v1/user/repos'
        r = http.request('POST', url, fields=data, headers=headers)

        assert r.status == 200

        r_data = json.loads(r.data.decode('utf-8'))

        print(r_data)


def create_user():
    data = {
        'email': 'test@test.com',
        'password': 'asdfasdfasdf!^3453',
        'username': 'user',
    }
    # user = NewUser(**data)
    r = http.request('POST', BASE_URL)


if __name__ == '__main__':
    r = http.request('GET', BASE_URL)
    assert r.status == 200

    user = GiteaUser('test', 'test12',
                     '9b329b9aaf76f6a469618a8a5ce9e3a577a33c0e')
    user.get_repositories()
