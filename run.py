from json import dumps
from pprint import pprint
from time import time

from requests import request


def event_fullfeed():
    print('event_fullfeed()')
    url = 'https://ls.sportradar.com/ls/feeds/?/betradar/en/Etc:UTC/gismo/event_fullfeed'
    json = get_json(url, 'event_fullfeed/')
    return json


def match(id):
    message = '    match({id:d})'.format(id=id)
    print(message)

    name = 'match/{id:d}'.format(id=id)

    url = 'https://ls.sportradar.com/ls/feeds/?/betradar/en/Etc:UTC/gismo/match_timeline/{id:d}'.format(id=id)
    get_json(url, name)

    url = 'https://ls.sportradar.com/ls/feeds/?/common/en/Etc:UTC/gismo/stats_match_situation/{id:d}'.format(id=id)
    get_json(url, name)


def get_json(url, name):
    response = request(method='GET', url=url)
    json = response.json()
    file = get_file(name)
    with open(file, 'w') as resource:
        contents = dumps(json)
        resource.write(contents)
    return json


def get_file(name):
    seconds = time()
    seconds = int(seconds)
    file = 'files/{name:s}-{seconds:d}'.format(name=name, seconds=seconds)
    return file


def main():
    json = event_fullfeed()
    for doc in json['doc']:
        for d in doc['data']:
            if d['_sid'] != 1:
                continue
            for category in d['realcategories']:
                for tournament in category['tournaments']:
                    for m in tournament['matches']:
                        if '_mclink' not in m or not m['_mclink']:
                            continue
                        id = m['_id']
                        match(id)


if __name__ == '__main__':
    main()
