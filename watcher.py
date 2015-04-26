#!/usr/bin/env python

import sys
from datetime import datetime
import requests

url = "https://api.github.com/users/{}/events"


def to_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")


def pluck(key, things):
    return [_[key] for _ in things]


def info_for(username):
    """Get one page of data (up to 30 actions)"""
    info = requests.get(url.format(username)).json()
    return info


def velocity_of(username):
    """Crude metric for GitHub activity"""
    info = info_for(username)
    date_strings = pluck('created_at', info)
    dates = [to_date(date_string) for date_string in date_strings]
    seconds = (dates[0] - dates[-1]).total_seconds()
    float_days = seconds / float(24 * 60 * 60)
    return len(dates) / float_days


def main():
    print("GITHUB VELOCITY (ACTIONS/DAY)")
    print("-----------------------------")
    for username in sys.argv[1:]:
        print("{}: {}".format(username, velocity_of(username)))

if __name__ == '__main__':
    main()
