import tool.utils as utils
from itertools import groupby
import maya
from tool.template import _Template
from tool.utils import config


class _Archive():           ##maybe rewrite a bit
    def __init__(self,post_list):
        self.month_group = []
        for key,group in groupby(post_list, key = lambda i:time_group_standard(i)):
            self.month_group.append(list(group))
        self.path_out = utils.join_path(config['Directory']['Output'], 'Archive/index.html')

    def build(self):
        new_div = utils.empty_soup.new_tag('div')
        for month in self.month_group:
            new_h2 = utils.empty_soup.new_tag('h2')
            if config['Config']['Archive_group_by'] == 'month':      ##need rewrite
                new_h2.string = str(month[0].meta.maya.datetime().strftime('%B %Y'))
            elif config['Config']['Archive_group_by'] == 'year':
                new_h2.string = str(month[0].meta.maya.datetime().strftime('%Y'))
            new_div.append(new_h2)
            new_ul = utils.empty_soup.new_tag('ul')
            for post in month:
                new_a = post.link
                new_li = utils.empty_soup.new_tag('li')
                new_li.append(new_a)
                new_ul.append(new_li)
            new_div.append(new_ul)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = 'Archive'
        archive_page = _Template('archive')
        archive_page.replace('%%Page_Title%%',str(new_title))
        archive_page.replace('%%Post_list%%',str(new_div))
        self.content = archive_page

    def print(self):
        self.build()
        return self.content.print()

def time_group_standard(post):     ##need rewrite
    if config['Config']['Archive_group_by'] == 'month':
        standard = post.meta.maya.datetime().strftime('%m/01/%Y')
    elif config['Config']['Archive_group_by'] == 'year':
        standard = post.meta.maya.datetime().strftime('01/01/%Y')
    return maya.parse(standard).epoch
