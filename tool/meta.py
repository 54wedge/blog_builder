import yaml
import maya
import tool.utils as utils
from tool.utils import config


class _Meta:
    def __init__(self,path):
        html_soup = utils.html_open(path,'soup')
        try:
            self.raw_meta = html_soup.find_all('code',class_ = 'meta')[0].get_text()
            if config['Config']['Hide_meta']:
                html_soup.find_all('code',class_ = 'meta')[0].parent.decompose()
        except IndexError:      #no meta data found
            print(utils.print_style(' **No raw meta found in ' + path, 'yellow', 'bold'))
            self.raw_meta = ''
        meta = yaml.safe_load(self.raw_meta)
        if meta is None:
            meta = {}
        if 'Title' in meta:
            self.title = meta['Title']
        else:
            try:
                self.title = html_soup.h1.get_text()
                meta['Title'] = self.title
                self.content_soup.h1.decompose()
            except AttributeError:
                self.title = 'Untitled'
                meta['Title'] = self.title
        if 'Author' in meta:
            self.author = meta['Author']
        else:
            self.author = config['Site']['Author']
            meta['Author'] = self.author
        if 'Date' in meta:
            self.maya = maya.parse(meta['Date'])
        else:
            self.maya = maya.MayaDT(utils.get_time(path,'modify'))
        self.date_epoch = self.maya.epoch          #for data comparason
        self.date_human = self.maya.datetime().strftime(config['Config']['Time_style'])
        meta['Date'] = self.date_human
        if 'Category' in meta:
            self.category = meta['Category']
        else:
            self.category = 'Default'
            meta['Category'] = self.category
        if 'Tag' in meta:
            meta['Tag'].sort(key = str.lower)
            self.tag = meta['Tag']
        else:
            self.tag = []
            meta['Tag'] = self.tag
        self.dict = meta
        self.content = html_soup.body
