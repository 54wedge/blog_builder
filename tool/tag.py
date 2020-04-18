import tool.utils as utils
from tool.template import _Template
from tool.utils import config
import tool.module as module


class _Tag:
    def __init__(self,tag_name,tag_list):
        self.tag_list = tag_list
        self.tag_name = tag_name
        self.path_out = utils.join_path(config['Directory']['Output'], 'tag', self.tag_name, 'index.html')

    def build(self):
        list_tag = module.post_list(self.tag_list)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = '#' + self.tag_name
        tag_page = _Template('tag')
        tag_page.replace('{&Page_Title&}', str(new_title))
        tag_page.replace('{$Tag$}',self.tag_name)
        tag_page.replace('{&Post_list&}',str(list_tag))
        tag_page.replace('../','../../')
        self.content = tag_page

    def print(self):
        self.build()
        return self.content.print()
