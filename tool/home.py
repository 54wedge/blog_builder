import tool.utils as utils
from tool.template import _Template
from tool.utils import config
import tool.module as module


class _Home:
    def __init__(self,post_list):
        self.post_list = post_list
        self.path_out = utils.join_path(config['Directory']['Output'], 'index.html')

    def build(self):
        list_home = module.home_list(self.post_list)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = 'Home'
        home_page = _Template('home')
        home_page.replace('{&Page_Title&}', str(new_title))
        home_page.replace('{&Post_list&}',str(list_home))
        home_page.replace('../','./')
        self.content = home_page

    def print(self):
        self.build()
        return self.content.print()
