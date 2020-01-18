from bs4 import BeautifulSoup as bs
import tool.io as io
import tool.builder as builder
from itertools import groupby
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
    def insert_body(self,template):
        soup = str_to_bs(self.content)
        body = soup.body
        if builder.get_config('Config','Hide_meta'):
            try:
                test = body.find_all('code','meta')[0].parent.decompose()
            except IndexError:      #no meta data found
                pass
        self.content = template.replace('%%Body%%',str(body))
    def insert_meta(self):
        for key in self.meta:
            if key == 'Category':        ##for future
                soup = str_to_bs('')
                category_path = '../category/' + self.meta[key] + '/index.html'
                category_link = a_href(self.meta[key],category_path)
                self.content = self.content.replace('%%'+key+'%%', str(category_link))
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
        template = _Template(self.type).print()
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
        elif type == 'archive':
            self.type = 'archive.html'
        elif type == 'category':
            self.type = 'category.html'
        elif type == 'tag':
            self.type = 'tag.html'
        else:
            raise TypeError('Failed to initialize _Template class. Missing or incorrect option')
        path_header = builder.get_config('Directory','Template') + 'header.html'
        path_footer = builder.get_config('Directory','Template') + 'footer.html'
        path = builder.get_config('Directory','Template') + self.type
        self.content = io.html_open(path_header) + io.html_open(path) + io.html_open(path_footer)
        soup = str_to_bs('')
        new_base = soup.new_tag('base', href = builder.get_config('Site','Prefix'))
        self.content = self.content.replace('%%Base%%', str(new_base))
    def print(self):
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

class _Archive():           ##maybe rewrite a bit
    def __init__(self):
        self.path_out = builder.get_config('Directory','Output') + 'Archive/index.html'
        self.post_list = builder.get_list('post')
        self.post_list.sort(key = lambda i:_Post(i).date_epoch, reverse = True)
        self.month_group = []
        for key,group in groupby(self.post_list, key = lambda i:time_group_standard(i)):
            self.month_group.append(list(group))
    def print(self):
        soup = str_to_bs('')
        new_div = soup.new_tag('div')
        for month in self.month_group:
            new_h2 = soup.new_tag('h2')
            if builder.get_config('Config','Archive_group_by') == 'month':
                new_h2.string = str(_Post(month[0]).maya.datetime().strftime('%B %Y'))
            elif builder.get_config('Config','Archive_group_by') == 'year':
                new_h2.string = str(_Post(month[0]).maya.datetime().strftime('%Y'))
            new_div.append(new_h2)
            new_ul = soup.new_tag('ul')
            for post_path in month:
                post = _Post(post_path)
                new_a = a_href(post.title,builder.relative_path(post.path_out))
                new_li = soup.new_tag('li')
                new_li.append(new_a)
                new_ul.append(new_li)
            new_div.append(new_ul)
        archive_page = _Template('archive').print()
        archive_page = archive_page.replace('%%Post_list%%',str(new_div))
        return archive_page

class _Category:
    def __init__(self):
        self.post_list = builder.get_list('post')
        self.post_list.sort(key = lambda i:_Post(i).date_epoch, reverse = True)
        self.category_dict = {}
        for post in self.post_list:
            if _Post(post).category in self.category_dict:
                self.category_dict[_Post(post).category].append(post)
            else:
                self.category_dict[_Post(post).category] = []
                self.category_dict[_Post(post).category].append(post)
    def print(self):
        soup = str_to_bs('')
        html_list = []
        for category_name, category_list in self.category_dict.items():
            new_div = soup.new_tag('div')
            new_ul = soup.new_tag('ul')
            for post_path in category_list:
                new_a = a_href(_Post(post_path).title,builder.relative_path(_Post(post_path).path_out))
                new_li = soup.new_tag('li')
                new_li.append(new_a)
                new_ul.append(new_li)
            new_div.append(new_ul)
            category_page = _Template('category').print()
            ## need edit html <title>
            category_page = category_page.replace('%%Category%%',category_name)
            category_page = category_page.replace('%%Post_list%%',str(new_div))
            html_list.append(category_page)
        return html_list

class _Tag():
    def __init__(self):
        self.post_list = builder.get_list('post')
        self.post_list.sort(key = lambda i:_Post(i).date_epoch, reverse = True)
        self.tag_dict = {}
        for post in self.post_list:
            for tag in _Post(post).tag:
                if tag in self.tag_dict:
                    self.tag_dict[tag].append(post)
                else:
                    self.tag_dict[tag] = []
                    self.tag_dict[tag].append(post)
        #print(self.tag_dict)
    def print(self):
        soup = str_to_bs('')
        html_list = []
        for tag_name, tag_list in self.tag_dict.items():
            new_div = soup.new_tag('div')
            new_ul = soup.new_tag('ul')
            for post_path in tag_list:
                new_a = a_href(_Post(post_path).title,builder.relative_path(_Post(post_path).path_out))
                new_li = soup.new_tag('li')
                new_li.append(new_a)
                new_ul.append(new_li)
            new_div.append(new_ul)
            tag_page = _Template('tag').print()
            ## need edit html <title>
            tag_page = tag_page.replace('%%Tag%%',tag_name)
            tag_page = tag_page.replace('%%Post_list%%',str(new_div))
            html_list.append(tag_page)
        return html_list

class _Index:
    pass

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

def time_group_standard(path):
    if builder.get_config('Config','Archive_group_by') == 'month':
        standard = _Post(path).maya.datetime().strftime('%m/01/%Y')
    elif builder.get_config('Config','Archive_group_by') == 'year':
        standard = _Post(path).maya.datetime().strftime('01/01/%Y')
    return maya.parse(standard).epoch
