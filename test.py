import json
import requests
import hashlib


def hash_url(url):
    hash_object = hashlib.md5()
    hash_object.update(url.encode('utf-8'))
    return hash_object.hexdigest()

if __name__ == '__main__':
    input_url = 'https://cdn.midjourney.com/a58089d8-c552-4620-a94d-0f9447531a97/0_0.png'
    resp = requests.get('http://172.17.1.169:8123/cors?url=' + input_url)
    headers = {'Content-Type': 'application/json'}

    resp = requests.post(
        'http://172.17.1.169:8124/depth', data=json.dumps({'img': resp.text.replace('data:image/png;base64,', ''),
                                                           'name': hash_url(input_url)}), headers=headers)

    print(resp.text)