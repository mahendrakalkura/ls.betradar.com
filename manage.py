from glob import glob
from json import dumps, loads
from pprint import pprint
from sys import argv
from time import time

from progressbar import ProgressBar
from requests import request


def download():
    while True:
        seconds = time()
        seconds = int(seconds)
        download_event_fullfeed(seconds)


def download_event_fullfeed(seconds):
    print('download_event_fullfeed()')
    url = 'https://ls.sportradar.com/ls/feeds/?/betradar/en/Etc:UTC/gismo/event_fullfeed'
    name = 'files/event_fullfeed/{seconds:d}.json'.format(seconds=seconds)
    json = fetch(url, name)
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
                        download_match(id, seconds)


def download_match(id, seconds):
    message = '    download_match({id:d})'.format(id=id)
    print(message)

    name = 'files/match_timeline/{id:d}-{seconds:d}.json'.format(id=id, seconds=seconds)
    url = 'https://ls.sportradar.com/ls/feeds/?/betradar/en/Etc:UTC/gismo/match_timeline/{id:d}'.format(id=id)
    fetch(url, name)

    name = 'files/stats_match_situation/{id:d}-{seconds:d}.json'.format(id=id, seconds=seconds)
    url = 'https://ls.sportradar.com/ls/feeds/?/common/en/Etc:UTC/gismo/stats_match_situation/{id:d}'.format(id=id)
    fetch(url, name)


def report(options):
    if options[0] == '--event-full-feed' and options[1] == '--statuses':
        report_event_full_feed_statuses()
    if options[0] == '--match-timeline' and options[1] == '--types':
        report_match_timeline_types()
    if options[0] == '--match-timeline' and options[1] == '--events':
        report_match_timeline_events(options[2])
    if options[0] == '--stats-match-situation':
        report_stats_match_situation(options[1])


def report_event_full_feed_statuses():
    statuses = set()
    files = glob('files/event_fullfeed/*.json')
    progress_bar = ProgressBar()
    for file in progress_bar(files):
        contents = None
        with open(file, 'r') as resource:
            contents = resource.read()
        if not contents:
            continue
        json = loads(contents)
        if not json:
            continue
        for doc in json['doc']:
            for d in doc['data']:
                if d['_sid'] != 1:
                    continue
                for category in d['realcategories']:
                    for tournament in category['tournaments']:
                        for m in tournament['matches']:
                            if '_mclink' not in m or not m['_mclink']:
                                continue
                            statuses.add(m['status']['name'])
    pprint(statuses)


def report_match_timeline_types():
    types = set()
    pattern = 'files/match_timeline/*.json'.format(id=id)
    files = glob(pattern)
    progress_bar = ProgressBar()
    for file in progress_bar(files):
        contents = None
        with open(file, 'r') as resource:
            contents = resource.read()
        if not contents:
            continue
        json = loads(contents)
        if not json:
            continue
        for d in json['doc']:
            for e in d['data']['events']:
                if 'coordinates' in e:
                    for c in e['coordinates']:
                        types.add(e['type'])
                else:
                    types.add(e['type'])
    pprint(types)


def report_match_timeline_events(id):
    pattern = 'files/match_timeline/{id:s}-*.json'.format(id=id)
    files = glob(pattern)
    progress_bar = ProgressBar()
    for file in progress_bar(files):
        contents = None
        with open(file, 'r') as resource:
            contents = resource.read()
        if not contents:
            continue
        json = loads(contents)
        if not json:
            continue
        events = []
        for d in json['doc']:
            for e in d['data']['events']:
                team = None
                if 'coordinates' in e:
                    for c in e['coordinates']:
                        x = c['X']
                        x = x / 100.
                        y = c['Y']
                        y = y / 100.
                        coordinates = (x, y,)
                        event = {
                            'team': c['team'],
                            'timestamp': e['uts'],
                            'coordinates': coordinates,
                            'description': e['type'],
                        }
                        events.append(event)
                else:
                    if 'team' in e and e['team']:
                        team = e['team']
                    coordinates = None
                    if 'X' in e and e['X'] and 'Y' in e and e['Y']:
                        x = e['X']
                        x = x / 100.
                        y = e['Y']
                        y = y / 100.
                        coordinates = (x, y,)
                    event = {
                        'team': team,
                        'timestamp': e['uts'],
                        'coordinates': coordinates,
                        'description': e['type'],
                    }
                    events.append(event)
    pprint(events)


def report_stats_match_situation(id):
    pattern = 'files/stats_match_situation/{id:s}-*.json'.format(id=id)
    files = glob(pattern)
    progress_bar = ProgressBar()
    for file in progress_bar(files):
        contents = None
        with open(file, 'r') as resource:
            contents = resource.read()
        if not contents:
            continue
        json = loads(contents)
        if not json:
            continue
        times = []
        for d in json['doc']:
            for e in d['data']['data']:
                times.append(e['time'])
        pprint(times)
        break


def fetch(url, name):
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


if __name__ == '__main__':
    if argv[1] == '--download':
        download()
    if argv[1] == '--report':
        report(argv[2:])
