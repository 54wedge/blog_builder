from tool.content import read_source
from tool.router import _Router
import tool.utils as utils
from tool.utils import config


class _Builder:
    def __init__(self):
        self.page_list = read_source(type = 'page')
        self.post_list = read_source(type = 'post')
        self.router = _Router(self.post_list)

    def build_page(self):
        print('Building pages......')
        for page in self.page_list:
            utils.safe_save(page.content, page.path)
            print(' --page '+ utils.print_style(page.path,'green') + ' is built')

    def build_post(self):
        print('Building posts......')
        for post in self.post_list:
            utils.safe_save(post.content, post.path)
            print(' --post ' + utils.print_style(post.path,'green') + ' is built')

    def build_router(self):
        utils.safe_save(self.router.home.content, self.router.home.path)
        print(' --Home page ' + utils.print_style(self.router.home.path,'green') + ' is built')
        utils.safe_save(self.router.archive.content, self.router.archive.path,)
        print(' --Archive page ' + utils.print_style(self.router.archive.path,'green') + ' is built')
        for category in self.router.category_list:
            utils.safe_save(category.content, category.path)
            print(' --Category page ' + utils.print_style(category.path,'green') + ' is built')
        for tag in self.router.tag_list:
            utils.safe_save(tag.content, tag.path)
            print(' --Tag page ' + utils.print_style(tag.path,'green') + ' is built')
