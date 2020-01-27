import tool.utils as utils

from bs4 import BeautifulSoup as bs

from tool.template import _Template


class _Category:
    def __init__(self,category_list):
        self.category_list = category_list
        self.category_name = self.category_list[0].meta.category
        self.path_out = utils.get_config('Directory','Output') + 'category/' + self.category_name + '/index.html'

    def print(self):
        soup = str_to_bs('')
        new_div = soup.new_tag('div')
        new_ul = soup.new_tag('ul')
        for post in self.category_list:
            new_a = post.link
            new_li = soup.new_tag('li')
            new_li.append(new_a)
            new_ul.append(new_li)
        new_div.append(new_ul)
        category_page = _Template('category').print()
        ## need edit html <title>
        category_page = category_page.replace('%%Category%%',self.category_name)
        category_page = category_page.replace('%%Post_list%%',str(new_div))
        category_page = category_page.replace('../','../../')
        return category_page


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
