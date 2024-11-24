import json


def scream(body: json) -> json:
    body['message'] = str.join(' ', [word.upper() for word in body['message'].split(' ')])

    return body
