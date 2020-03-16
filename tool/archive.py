import tool.utils as utils
from itertools import groupby
import maya
from tool.template import _Template
from tool.utils import config
import tool.gen_list as gen_list


class _Archive():
    def __init__(self,post_list):
        self.post_list = post_list
        self.path_out = utils.join_path(config['Directory']['Output'], 'Archive/index.html')

    def build(self):
        list_archive = gen_list.archive(self.post_list)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = 'Archive'
        archive_page = _Template('archive')
        archive_page.replace('{&Page_Title&}',str(new_title))
        archive_page.replace('{&Post_list&}',str(list_archive))
        self.content = archive_page

    def group_standard(self, post):
        if config['Config']['Archive_group_by'] == 'month':
            standard = post.meta.maya.datetime().strftime('%m/01/%Y')
        elif config['Config']['Archive_group_by'] == 'year':
            standard = post.meta.maya.datetime().strftime('01/01/%Y')
        return maya.parse(standard).epoch

    def print(self):
        self.build()
        return self.content.print()
