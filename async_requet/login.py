import requests
from requests.exceptions import Timeout

from async_requet.exeptions import RequestException


def login(username, password, url):
    response = None
    headers = {
        'Accept': 'application/json',
    }
    data = {
    'j_username': username,
    'j_password': password,
    'security_answer': 'undefined',
    'portal_name': 'accoffmngr'
    }
    url = url

    try:
        response = requests.post(url=url, headers=headers, data=data, timeout=2)
    except Timeout:
        raise RequestException('Login to async_requet fails due to timeout')

    if response.status_code != 200:
        raise RequestException(
            'Login Request Fail, status: {}'.format(response.status_code)
        )

    headers = response.headers
    cookie = headers['Set-Cookie']

    return cookie
