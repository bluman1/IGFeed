""" Author and finisher of this script is Michael on 17/09/2016 """
import urllib

import re
import requests
from bs4 import BeautifulSoup
import urllib.request


def get_latest_image(feed_name):
    url = 'https://www.instagram.com/'+feed_name+'/'
    r = urllib.request.urlopen(url)
    t = r.read()
    t = str(t)
    soup = BeautifulSoup(t)
    body = soup.find('body')
    scripts = body.find_all('script')
    script = scripts[2]
    script_content = script.get_text()
    length = len(script_content)
    ig_json = script_content[20:length-1].strip()
    reg = re.compile(r'("thumbnail_src": "[$-/:-?{-~!^_`\[\]a-zA-Z0-9]+")')
    mo = reg.search(ig_json)
    thumbnail = mo.group(1)
    length = len(thumbnail)
    thumbnail = thumbnail[18:length-1]
    url = ''
    for c in thumbnail:
        if c is not '?':
            url += c
        else:
            break
    image_url = url
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
