import tool.utils as utils

from bs4 import BeautifulSoup as bs

from tool.template import _Template
from tool.meta import _Meta

class _Page:
    def __init__(self,path):
        self.path = path
        self.path_out = utils.in_to_out(path)
        self.type = 'page'
        html_soup = utils.html_open(path,'soup')
        try:
            raw_meta = html_soup.find_all('code',class_ = 'meta')[0].get_text()
            html_soup.find_all('code',class_ = 'meta')[0].parent.decompose()
        except IndexError:      #no meta data found
            print('No raw meta found in %s' %path)
            raw_meta = ''
        self.content_soup = html_soup.body
        self.meta = _Meta(raw_meta,path)
        self.link = a_href(self.meta.title,utils.relative_path(self.path_out))

    def print(self):
        template = _Template(self.type).print()
        self.content = template.replace('%%Body%%',str(self.content_soup))
        for key in self.meta.dict:
            if key == 'Category':        ##for future
                category_path = '../category/' + self.meta.dict[key] + '/index.html'
                category_link = a_href(self.meta.dict[key],category_path)
                self.content = self.content.replace('%%'+key+'%%', str(category_link))
            elif key == 'Tag':
                soup = str_to_bs('')
                new_span = soup.new_tag('span',id = 'tag')
                for tag in self.meta.dict['Tag']:
                    tag_path = '../tag/' + tag + '/index.html'
                    tag_link = a_href('#' + tag,tag_path)
                    new_span.append(tag_link)
                soup.append(new_span)
                self.content = self.content.replace('%%'+key+'%%', str(soup))
            else:
                self.content = self.content.replace('%%'+key+'%%', self.meta.dict[key])
        #self.insert_meta()
        return self.content

def a_href(name,path):
    soup = bs('','lxml')
    new_a = soup.new_tag('a',href = path)
    new_a.string = name
    return new_a

def str_to_bs(html):
    if type(html) is bs:
        return html
    else:
        soup = bs(html,'lxml')
        return soup
