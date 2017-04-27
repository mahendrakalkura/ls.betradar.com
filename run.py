from json import dumps
from time import time

from requests import request


def event_fullfeed(seconds):
    print('event_fullfeed()')
    url = 'https://ls.sportradar.com/ls/feeds/?/betradar/en/Etc:UTC/gismo/event_fullfeed'
    name = 'files/event_fullfeed/{seconds:d}.json'.format(seconds=seconds)
    json = get_json(url, name)
    if not json:
        return
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
                        match(id, seconds)


def match(id, seconds):
    message = '    match({id:d})'.format(id=id)
    print(message)

    name = 'files/match_timeline/{id:d}-{seconds:d}.json'.format(id=id, seconds=seconds)
    url = 'https://ls.sportradar.com/ls/feeds/?/betradar/en/Etc:UTC/gismo/match_timeline/{id:d}'.format(id=id)
    get_json(url, name)

    name = 'files/stats_match_situation/{id:d}-{seconds:d}.json'.format(id=id, seconds=seconds)
    url = 'https://ls.sportradar.com/ls/feeds/?/common/en/Etc:UTC/gismo/stats_match_situation/{id:d}'.format(id=id)
    get_json(url, name)


def get_json(url, name):
    response = None
    try:
        response = request(method='GET', url=url)
    except Exception:
        pass
    if not response:
        return
    json = response.json()
    with open(name, 'w') as resource:
        contents = dumps(json, indent=4, sort_keys=True)
        resource.write(contents)
    return json


def main():
    seconds = time()
    seconds = int(seconds)
    while True:
        event_fullfeed(seconds)


if __name__ == '__main__':
    main()
