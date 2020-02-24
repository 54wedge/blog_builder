import tool.utils as utils
from tool.template import _Template
from tool.utils import config


class _Category:
    def __init__(self,category_list):
        self.category_list = category_list
        self.category_name = self.category_list[0].meta.category
        self.path_out = utils.join_path(config['Directory']['Output'], 'category', self.category_name, 'index.html')

    def build(self):
        new_div = utils.empty_soup.new_tag('div')
        new_ul = utils.empty_soup.new_tag('ul')
        for post in self.category_list:
            new_a = post.link
            new_li = utils.empty_soup.new_tag('li')
            new_li.append(new_a)
            new_ul.append(new_li)
        new_div.append(new_ul)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = self.category_name
        category_page = _Template('category')
        category_page.replace('%%Page_Title%%', str(new_title))
        category_page.replace('%%Category%%',self.category_name)
        category_page.replace('%%Post_list%%',str(new_div))
        category_page.replace('../','../../')
        self.content = category_page

    def print(self):
        self.build()
        return self.content.print()
