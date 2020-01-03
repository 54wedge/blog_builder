from bs4 import BeautifulSoup as bs
import tool.io as io
import tool.builder as builder

import yaml
import maya

class _Page:
    def __init__(self,path):
        self.path = path
        self.path_out = builder.remove_page_index(builder.in_to_out(self.path))
        self.name = builder.get_name(path)
        self.type = 'page'
        self.content = io.html_open(path)

        self.meta = self.get_meta()
        #print(self.meta)
        #print(self.content)
    def insert_body(self,template):
        soup = str_to_bs(self.content)
        #print(soup)
        body = soup.body
        #print(self.content)
        #print(self.path)
        #print(body)
        if builder.get_config('Config','Hide_meta'):
            try:
                test = body.find_all('code','meta')[0].parent.decompose()
            except IndexError:      #no meta data found
                pass
        self.content = template.replace('%%Body%%',str(body))
    def insert_meta(self):
        for key in self.meta:
            if key == 'Category':        ##for future
                self.content = self.content.replace('%%'+key+'%%', self.meta[key])
            elif key == 'Tag':
                soup = str_to_bs('')
                for tag in self.meta[key]:
                    new_span = soup.new_tag('span',id = 'tag')
                    new_span.string = '#' + tag
                    soup.append(new_span)
                self.content = self.content.replace('%%'+key+'%%', str(soup))
            else:
                self.content = self.content.replace('%%'+key+'%%', self.meta[key])
    def get_meta(self):        ##rewrite
        soup = str_to_bs(self.content)
        try:
            raw_meta = soup.find_all('code','meta')[0].get_text()
            meta = yaml.safe_load(raw_meta)
        except IndexError:      #no meta data found
            meta = {}
        except yaml.scanner.ScannerError:
            print('double check yaml format of %s' % self.path)
            meta = {}
        if 'Title' in meta:
            self.title = meta['Title']
            try:
                soup = str_to_bs(self.content)
                soup.h1.decompose()           #try to clean extra the first <h1>
                self.content = str(soup)
                #print(self.content)
            except AttributeError:
                pass
        else:
            try:
                soup = str_to_bs(self.content)
                self.title = soup.h1.get_text()
                meta['Title'] = self.title
                soup.h1.decompose()
                self.content = str(soup)
            except AttributeError:
                self.title = 'Untitled'
                meta['Title'] = self.title
        if 'Author' in meta:
            self.author = meta['Author']
        else:
            self.author = builder.get_config('Site','Author')
            meta['Author'] = self.author
        if 'Date' in meta:
            self.maya = maya.parse(meta['Date'])
        else:
            self.maya = maya.MayaDT(builder.get_time(self.path,'modify'))
        self.date_epoch = self.maya.epoch          #for data comparason
        self.date = self.maya.datetime().strftime(builder.get_config('Config','Time_style'))
        meta['Date'] = self.date
        return meta

    def print(self):
        template = _Template(self.type).output()
        self.insert_body(template)
        self.insert_meta()
        return self.content
'''
    def __repr__(self):
        return repr((self.title,self.date))
'''

class _Post(_Page):
    def __init__(self,path):
        _Page.__init__(self,path)
        self.path_out = builder.in_to_out(self.path)
        self.type = 'post'
        if 'Category' in self.meta:
            self.category = self.meta['Category']
        else:
            self.category = 'Default'
            self.meta['Category'] = self.category
        if 'Tag' in self.meta:
            self.tag = self.meta['Tag']
        else:
            self.tag = []
            self.meta['Tag'] = self.tag

class _Template():
    def __init__(self,type = None):
        if type == 'page':
            self.type = 'page.html'
        elif type == 'post':
            self.type = 'post.html'
        else:
            raise TypeError('Failed to initialize _Template class. Missing or incorrect option')
        path_header = builder.get_config('Directory','Template') + 'header.html'
        path_footer = builder.get_config('Directory','Template') + 'footer.html'
        path = builder.get_config('Directory','Template') + self.type
        self.content = io.html_open(path_header) + io.html_open(path) + io.html_open(path_footer)
    def output(self):
        soup = str_to_bs('')
        new_a = a_href('Index','../index.html')
        new_nav = soup.new_tag('nav',id = 'nav-menu' )
        soup.append(new_nav)
        soup.nav.append(new_a)
        page_list = builder.get_list('page')
        for i in page_list:
            name = builder.get_name(i)
            path = '../' + name + '/index.html'
            new_a = a_href(name,path)
            soup.nav.append(new_a)
        self.content = self.content.replace('%%Nav%%',str(soup))
        return self.content

#def get_abstract(html):

def a_href(name,path):
    soup = bs('','html.parser')
    new_a = soup.new_tag('a',href = path)
    new_a.string = name
    return new_a

def str_to_bs(html):
    if type(html) is bs:
        return html
    else:
        soup = bs(html,'html.parser')
        return soup
