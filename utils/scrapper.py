# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup as BS


def parse_sitemap(url):
    f = urllib2.urlopen(url)
    data = BS(f.read())
    links = [x.text for x in data.body.find_all('loc')]
    return links


def find_location(slug):
    url = 'https://civilhub.org/sitemap.xml'
    links = [x for x in parse_sitemap(url) if 'sitemap-locations' in x]
    locations = []
    for link in links:
        locations += [x for x in parse_sitemap(link) if slug in x]
    return locations
