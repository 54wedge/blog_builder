import yaml
import maya
import tool.utils as utils


class _Meta:
    def __init__(self,raw_meta,path):
        meta = yaml.safe_load(raw_meta)
        if meta is None:
            meta = {}
        if 'Title' in meta:
            self.title = meta['Title']
        else:
            soup = utils.html_open(path,'soup')
            try:
                self.title = soup.h1.get_text()
                meta['Title'] = self.title
            except AttributeError:
                self.title = 'Untitled'
                meta['Title'] = self.title
        if 'Author' in meta:
            self.author = meta['Author']
        else:
            self.author = utils.get_config('Site','Author')
            meta['Author'] = self.author
        if 'Date' in meta:
            self.maya = maya.parse(meta['Date'])
        else:
            self.maya = maya.MayaDT(utils.get_time(path,'modify'))
        self.date_epoch = self.maya.epoch          #for data comparason
        self.date_human = self.maya.datetime().strftime(utils.get_config('Config','Time_style'))
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
