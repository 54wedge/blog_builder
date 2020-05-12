from tool.content import read_source
from tool.router import _Router
import tool.utils as utils
from tool.utils import config


class _Builder:
    def __init__(self):
        self.page_list = read_source(type = 'page')
        self.post_list = read_source(type = 'post')
        self.router = _Router(self.post_list)
        self.save_style = config['Config']['Save_style']

    def build_page(self):
        print('Building pages......')
        for page in self.page_list:
            utils.safe_save(page.struct.content, page.struct.path, self.save_style)
            print(' --page '+ utils.print_style(page.path,'green') + ' is built')

    def build_post(self):
        print('Building posts......')
        for post in self.post_list:
            utils.safe_save(post.struct.content, post.struct.path, self.save_style)
            print(' --post ' + utils.print_style(post.path,'green') + ' is built')

    def build_router(self):
        utils.safe_save(self.router.home.struct.content, self.router.home.struct.path, self.save_style)
        print(' --Home page ' + utils.print_style(self.router.home.struct.path,'green') + ' is built')
        utils.safe_save(self.router.archive.struct.content, self.router.archive.struct.path, self.save_style)
        print(' --Archive page ' + utils.print_style(self.router.archive.struct.path,'green') + ' is built')
        for category in self.router.category_list:
            utils.safe_save(category.content, category.path, self.save_style)
            print(' --Category page ' + utils.print_style(category.path,'green') + ' is built')
        for tag in self.router.tag_list:
            utils.safe_save(tag.content, tag.path, self.save_style)
            print(' --Tag page ' + utils.print_style(tag.path,'green') + ' is built')
