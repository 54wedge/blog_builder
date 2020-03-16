import tool.utils as utils
from tool.template import _Template
from tool.utils import config


class _Home:
    def __init__(self,post_list):
        self.post_list = post_list
        self.path_out = utils.join_path(config['Directory']['Output'], 'index.html')

    def get_abstract(self,post):
        try:
            abstract = post.meta.dict['Abstract']
        except KeyError:
            body = post.meta.content
            if '<!--more-->' in str(body):
                abstract = str(body).split('<!--more-->')[0]
                abstract = utils.str_to_bs(abstract)
                abstract = abstract.get_text()
            else:
                abstract = 'No abstract provided'
        return abstract

    def build(self):
        new_div = utils.empty_soup.new_tag('div')
        for post in self.post_list:
            new_a = post.link
            new_ul = utils.empty_soup.new_tag('ul')
            new_li = utils.empty_soup.new_tag('li')
            new_li.append(new_a)
            new_div_2 = utils.empty_soup.new_tag('div')
            new_div_2.string = self.get_abstract(post)
            new_li.append(new_a)
            new_li.append(new_div_2)
            new_ul.append(new_li)
            new_div.append(new_ul)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = 'Home'
        home_page = _Template('home')
        home_page.replace('{&Page_Title&}', str(new_title))
        home_page.replace('{&Post_list&}',str(new_div))
        home_page.replace('../','./')
        self.content = home_page

    def print(self):
        self.build()
        return self.content.print()
