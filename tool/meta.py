from yaml import safe_load as read_meta
from datetime import datetime
from dateutil import parser as dtparser
from tool.utils import nsprint, sstyle
from tool.config import config
from os import path as ospath
from bs4 import BeautifulSoup as bs

class _Meta:
    def __init__(self, path):
        with open(path,'r') as html:
            html = html.read()
        html_soup = bs(html,'lxml')
        try:
            self.raw_meta = html_soup.find_all('code',class_ = 'meta')[0].get_text()
            if config.hide_meta:
                html_soup.find_all('code',class_ = 'meta')[0].parent.decompose()
        except IndexError:      #no meta data found
            nsprint(sstyle(' **No raw meta found in ' + path, 'yellow', 'bold'))
            self.raw_meta = ''
        meta = read_meta(self.raw_meta)
        if meta is None:
            meta = {}
        if 'Title' in meta:
            self.title = meta['Title']
        else:
            try:
                self.title = html_soup.h1.get_text()
                meta['Title'] = self.title
                html_soup.h1.decompose()
            except AttributeError:
                self.title = 'Untitled'
                meta['Title'] = self.title
        if 'Author' in meta:
            self.author = meta['Author']
        else:
            self.author = config.site_author
            meta['Author'] = self.author
        if 'Date' in meta:
            self.datetime = dtparser.parse(meta["Date"])
        else:
            if config.time_by == 'modify':
                self.datetime = datetime.fromtimestamp(ospath.getmtime(path))
            elif config.time_by == 'create':
                self.datetime = datetime.fromtimestamp(ospath.getctime(path))
        self.datetime_epoch = self.datetime.timestamp()          #for data comparason
        self.datetime_human = self.datetime.strftime(config.time_style)
        meta['Date'] = self.datetime_human
        if 'Category' in meta:
            self.category = meta['Category'].capitalize()
        else:
            self.category = 'Default'
            meta['Category'] = self.category
        if 'Tag' in meta:
            meta['Tag'].sort(key = str.lower)
            for i in range(len(meta['Tag'])):
                meta['Tag'][i] = meta['Tag'][i].capitalize()
            self.tag = meta['Tag']
        else:
            self.tag = []
            meta['Tag'] = self.tag
        self.dict = meta
        self.body = html_soup.body

def str_to_bs(html):
    soup = bs(html,'lxml')
    return soup

empty_soup = bs('','lxml')