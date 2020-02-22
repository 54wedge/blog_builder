import tool.utils as utils
from itertools import groupby
import maya
from tool.template import _Template


class _Archive():           ##maybe rewrite a bit
    def __init__(self,post_list):
        self.month_group = []
        for key,group in groupby(post_list, key = lambda i:time_group_standard(i)):
            self.month_group.append(list(group))
        self.path_out = utils.join_path(utils.get_config('Directory','Output'), 'Archive/index.html')

    def build(self):
        soup = utils.str_to_bs('')
        new_div = soup.new_tag('div')
        for month in self.month_group:
            new_h2 = soup.new_tag('h2')
            if utils.get_config('Config','Archive_group_by') == 'month':      ##need rewrite
                new_h2.string = str(month[0].meta.maya.datetime().strftime('%B %Y'))
            elif utils.get_config('Config','Archive_group_by') == 'year':
                new_h2.string = str(month[0].meta.maya.datetime().strftime('%Y'))
            new_div.append(new_h2)
            new_ul = soup.new_tag('ul')
            for post in month:
                new_a = post.link
                new_li = soup.new_tag('li')
                new_li.append(new_a)
                new_ul.append(new_li)
            new_div.append(new_ul)
        archive_page = _Template('archive')
        archive_page.replace('%%Post_list%%',str(new_div))
        self.content = archive_page

    def print(self):
        self.build()
        return self.content.print()

def time_group_standard(post):     ##need rewrite
    if utils.get_config('Config','Archive_group_by') == 'month':
        standard = post.meta.maya.datetime().strftime('%m/01/%Y')
    elif utils.get_config('Config','Archive_group_by') == 'year':
        standard = post.meta.maya.datetime().strftime('01/01/%Y')
    return maya.parse(standard).epoch
