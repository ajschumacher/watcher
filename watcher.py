#!/usr/bin/env python

import sys
from datetime import datetime
import requests

url = "https://api.github.com/users/{}/events"


def to_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")


def info_for(username):
    """Get one page of data (up to 30 actions)"""
    info = requests.get(url.format(username)).json()
    return info


def velocity_of(username):
    """Crude metric for GitHub activity"""
    info = info_for(username)
    date_strings = [_['created_at'] for _ in info]
    dates = [to_date(date_string) for date_string in date_strings]
    earliest = min(dates)
    now = datetime.now()
    seconds = (now - earliest).total_seconds()
    float_days = seconds / float(24 * 60 * 60)
    return len(dates) / float_days


def header():
    print("GITHUB VELOCITY (ACTIONS/DAY)")
    print("-----------------------------")

def show(user, score):
    print("  {:<20}{:>5.1f}".format(user, score))

def main():
    scores = []
    header()
    for username in sys.argv[1:]:
        score = velocity_of(username)
        show(username, score)
        scores.append((username, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    print('')
    header()
    for username, score in scores:
        show(username, score)

if __name__ == '__main__':
    main()
