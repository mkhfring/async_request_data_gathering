import requests


def login(username, password, url):
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

    response = requests.post(url=url, headers=headers, data=data)
    headers = response.headers
    cookie = headers['Set-Cookie']

    return cookie
