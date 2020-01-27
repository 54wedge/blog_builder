from tool.page import _Page
from tool.post import _Post
from tool.index import _Index
from tool.archive import _Archive
from tool.category import _Category
from tool.tag import _Tag

import tool.utils as utils

#scan post html
class _Builder:
    def __init__(self):
        self.post_list = []
        self.page_list = []
        for page_path in utils.get_list('page'):
            self.page_list.append(_Page(page_path))
        for post_path in utils.get_list('post'):
            self.post_list.append(_Post(post_path))
        self.post_list.sort(key = lambda i:i.meta.date_epoch, reverse = True)
        short_post_list = self.post_list[0:utils.get_config('Index','Page_size')]
        #print(short_post_list)
        self.index = _Index(short_post_list)
        self.archive = _Archive(self.post_list)
        self.category_dict = {}
        self.tag_dict = {}
        for post in self.post_list:
            if post.meta.category in self.category_dict:
                self.category_dict[post.meta.category].append(post)
            else:
                self.category_dict[post.meta.category] = []
                self.category_dict[post.meta.category].append(post)
            for meta_tag in post.meta.tag:
                if meta_tag in self.tag_dict:
                    self.tag_dict[meta_tag].append(post)
                else:
                    self.tag_dict[meta_tag] = []
                    self.tag_dict[meta_tag].append(post)
        for key in self.category_dict:
            self.category_dict[key] = _Category(self.category_dict[key])
        for key in self.tag_dict:
            self.tag_dict[key] = _Tag(key,self.tag_dict[key])

    def build_page(self):
        for page in self.page_list:
            utils.save(page.print(),page.path_out,'prettify')

    def build_post(self):
        for post in self.post_list:
            utils.save(post.print(),post.path_out,'prettify')

    def build_index(self):
        utils.save(self.index.print(),self.index.path_out,'prettify')

    def build_archive(self):
        utils.save(self.archive.print(),self.archive.path_out,'prettify')

    def build_category(self):
        for category in self.category_dict.values():
            utils.save(category.print(),category.path_out,'prettify')

    def build_tag(self):
        for tag in self.tag_dict.values():
            utils.save(tag.print(),tag.path_out,'prettify')
