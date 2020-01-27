import tool.utils as utils

from bs4 import BeautifulSoup as bs

from tool.template import _Template


class _Index:
    def __init__(self,post_list):
        self.post_list = post_list
        self.path_out = utils.get_config('Directory','Output') + '/index.html'
    def print(self):
        soup = str_to_bs('')
        index_page = _Template('index').print()
        new_div = soup.new_tag('div')
        for post in self.post_list:
            new_a = post.link
            new_ul = soup.new_tag('ul')
            new_li = soup.new_tag('li')
            new_li.append(new_a)
            new_div_2 = soup.new_tag('div')
            new_div_2.string = self.get_abstract(post)
            new_li.append(new_a)
            new_li.append(new_div_2)
            new_ul.append(new_li)
            new_div.append(new_ul)
        index_page = index_page.replace('%%Post_list%%',str(new_div))
        index_page = index_page.replace('../','./')
        return index_page
    def get_abstract(self,post):
        #print(path)
        try:
            abstract = post.meta.dict['Abstract']
        except KeyError:
            html = utils.html_open(post.path,'soup')
            body = html.body
            #print(body)
            try:
                body.find_all('code',class_ = 'meta')[0].parent.decompose()
            except IndexError:      #no meta data found
                pass
            #body = body.get_text()
            if '<!--more-->' in str(body):
                abstract = str(body).split('<!--more-->')[0]
                abstract = str_to_bs(abstract)
                abstract = abstract.get_text()
            else:
                abstract = 'No abstract provided'
        return abstract

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
