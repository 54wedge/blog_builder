from tool.content import _Content
from tool.home import _Home
from tool.archive import _Archive
from tool.category import _Category
from tool.tag import _Tag

import tool.utils as utils
from tool.utils import config


class _Builder:
    def __init__(self):
        self.post_list = []
        self.page_list = []
        for page_path in utils.get_list('page'):
            self.page_list.append(_Content(page_path,'page'))
        for post_path in utils.get_list('post'):
            self.post_list.append(_Content(post_path,'post'))
        self.post_list.sort(key = lambda i:i.meta.date_epoch, reverse = True)
        self.save_style = config['Config']['Save_style']

    def build_page(self):
        print('Building pages......')
        for page in self.page_list:
            utils.safe_save(page.print(), page.path, self.save_style)
            print(' --page '+ utils.print_style(page.path,'green') + ' is built')

    def build_post(self):
        print('Building posts......')
        for post in self.post_list:
            utils.safe_save(post.print(), post.path, self.save_style)
            print(' --post ' + utils.print_style(post.path,'green') + ' is built')

    def build_home(self):
        print('Building Home page......')
        short_post_list = self.post_list[0:config['Home']['Page_size']]
        self.home = _Home(short_post_list)
        utils.safe_save(self.home.print(),self.home.path_out,self.save_style)
        print(' --Home page ' + utils.print_style(self.home.path_out,'green') + ' is built')

    def build_archive(self):
        print('Building Archive page......')
        self.archive = _Archive(self.post_list)
        utils.safe_save(self.archive.print(), self.archive.path_out, self.save_style)
        print(' --Archive page ' + utils.print_style(self.archive.path_out,'green') + ' is built')

    def build_category(self):
        print('Building Category pages......')
        self.category_dict = {}
        for post in self.post_list:
            if post.meta.category in self.category_dict:
                self.category_dict[post.meta.category].append(post)
            else:
                self.category_dict[post.meta.category] = []
                self.category_dict[post.meta.category].append(post)
        for key in self.category_dict:
            self.category_dict[key] = _Category(self.category_dict[key])
        for category in self.category_dict.values():
            utils.safe_save(category.print(), category.path_out, self.save_style)
            print(' --Category page ' + utils.print_style(category.path_out,'green') + ' is built')

    def build_tag(self):
        print('Building Tag pages......')
        self.tag_dict = {}
        for post in self.post_list:
            for meta_tag in post.meta.tag:
                if meta_tag in self.tag_dict:
                    self.tag_dict[meta_tag].append(post)
                else:
                    self.tag_dict[meta_tag] = []
                    self.tag_dict[meta_tag].append(post)
        for key in self.tag_dict:
            self.tag_dict[key] = _Tag(key,self.tag_dict[key])
        for tag in self.tag_dict.values():
            utils.safe_save(tag.print(), tag.path_out, self.save_style)
            print(' --Tag page ' + utils.print_style(tag.path_out,'green') + ' is built')
