#!/usr/bin/env python

import sys
from datetime import datetime, timedelta
import requests

url = "https://api.github.com/users/{}/events"
interval = timedelta(days=14)


def to_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")


def float_days(interval):
    interval_seconds = interval.total_seconds()
    interval_days = interval_seconds / float(24 * 60 * 60)
    return interval_days


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
    then = now - interval
    if earliest < then:
        # crop off old actions and accept default period
        dates = [date for date in dates if then <= date]
        this_interval = interval
    else:
        # period is shorter than the default
        this_interval = now - earliest
    return len(dates) / float_days(this_interval)


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
