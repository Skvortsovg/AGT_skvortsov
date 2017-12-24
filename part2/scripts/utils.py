# -*- coding: utf-8 -*-
import urllib
import urllib.request
import json
import time


def get_json(url):
    getjson = urllib.request.urlopen(url).read().decode('utf-8')
    getjson = json.loads(getjson)
    time.sleep(0.3)
    return getjson