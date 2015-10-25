#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import argparse
import requests


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--endpoint', default='http://127.0.0.1:8001/api/update')
    args = parser.parse_args(argv)
    requests.post(args.endpoint, data=json.dumps({'device_code': 'aaaa', 'hit': 'true'}))

if __name__ == '__main__':
    main()
