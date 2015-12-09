#!/usr/bin/env python
# coding: utf-8

import re
import requests

_STATES = (
    'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI',
    'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
    'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR',
    'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY')


def extract_stations():
    stations = []
    stations_set = ()
    for state in _STATES:
        print('Downloading %s stations' % state)
        req = requests.get(
            'http://jaws.pbs.org/localization/member/state/%s/' % state)
        for station_info in req.json()['stations_list']:
            callsign = station_info['callsign']
            if callsign in stations_set:
                print('WARNING! %s already processed' % callsign)
                continue
            print('Downloading %s station' % callsign)
            req = requests.get(
                'http://jaws.pbs.org/localization/true/?callsign=%s' % callsign)
            station = req.json()['station']
            site_address = station['site_address']
            if not site_address:
                print('WARNING! %s has no site address' % callsign)
                continue
            common_name = station['common_name']
            mobj = re.search(
                r'^(?:(?:https?:)?//)?(?:[^/]+\.)?([^/]+\.[^/]+)(?:/|$)', site_address)
            if not mobj:
                print('WARNING! Unable to extract site address part for %s' % callsign)
            stations.append({
                'callsign': callsign,
                'name': common_name,
                'site': site_address,
                'part': mobj.group(1) if mobj else None,
            })
    return stations


def write_ytdl_tuple(stations):
    with open('stations', 'w') as f:
        f.writelines('_STATIONS = (\n')
        for s in stations:
            f.writelines(
                "    ('%s', '%s (%s)'),  # %s\n"
                % (s['part'], s['name'], s['callsign'], s['site']))
        f.writelines(')\n')


def main():
    write_ytdl_tuple(extract_stations())

if __name__ == '__main__':
    main()
