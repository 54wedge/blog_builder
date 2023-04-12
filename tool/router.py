import tool.utils as utils
from tool.template import _Template
from tool.utils import content_path
import tool.module as module

class _Router():
    def __init__(self,config, post_list):
        self.config = config
        self.post_list = post_list
        self.home = _Home(config, post_list)
        self.archive = _Archive(config, post_list)
        self.category_list = _Category(config, post_list).list()
        self.tag_list = _Tag(config, post_list).list()

class _Home:
    def __init__(self,config, post_list):
        self.config = config
        self.post_list = post_list[0:config['Site']['Home_Page_Items']]
        self.path = utils.join_path(config['Directory']['Output'], 'index.html')
        self.content = self.build()

    def build(self):
        list_home = module.home_module(self.post_list)
        home_page = _Template(self.config, 'home')
        home_page.replace('{$Page_Title$}', 'Home')
        home_page.replace('{&Home_module&}',str(list_home))
        home_page.replace('../','./')
        return home_page.str()

class _Archive():
    def __init__(self,config, post_list):
        self.config = config
        self.post_list = post_list
        self.path = utils.join_path(config['Directory']['Output'], 'Archive/index.html')
        self.content = self.build()

    def build(self):
        list_archive = module.archive_module(self.config['Site']['Archive_group_by'], self.post_list)
        archive_page = _Template(self.config, 'archive')
        archive_page.replace('{$Page_Title$}', 'Archive')
        archive_page.replace('{&Archive_module&}',str(list_archive))
        return archive_page.str()

class _Category:
    def __init__(self,config, post_list):
        self.config = config
        self.category_dict = {}
        for post in post_list:
            try:
                self.category_dict[post.meta.category].append(post)
            except KeyError:
                self.category_dict[post.meta.category] = []
                self.category_dict[post.meta.category].append(post)

    def build(self, category_list, category_name):
        list_category = module.post_module(category_list)
        category_page = _Template(self.config, 'category')
        category_page.replace('{$Page_Title$}', category_name)
        category_page.replace('{$Category$}', category_name)
        category_page.replace('{&Post_module&}',str(list_category))
        category_page.replace('../','../../')
        return category_page.str()

    def list(self):
        list = []
        for category_name in self.category_dict.keys():
            category_list = self.category_dict[category_name]
            content = self.build(category_list, category_name)
            path = utils.join_path(self.config['Directory']['Output'], 'category', category_name, 'index.html')
            struct = content_path(content, path)
            list.append(struct)
        return list

class _Tag:
    def __init__(self,config, post_list):
        self.config = config
        self.tag_dict = {}
        for post in post_list:
            for meta_tag in post.meta.tag:
                try:
                    self.tag_dict[meta_tag].append(post)
                except KeyError:
                    self.tag_dict[meta_tag] = []
                    self.tag_dict[meta_tag].append(post)

    def build(self, tag_list, tag_name):
        list_tag = module.post_module(tag_list)
        tag_page = _Template(self.config, 'tag')
        tag_page.replace('{$Page_Title$}', '#' + tag_name)
        tag_page.replace('{$Tag$}', tag_name)
        tag_page.replace('{&Post_module&}',str(list_tag))
        tag_page.replace('../','../../')
        return tag_page.str()

    def list(self):
        list = []
        for tag_name in self.tag_dict.keys():
            tag_list = self.tag_dict[tag_name]
            content = self.build(tag_list, tag_name)
            path = utils.join_path(self.config['Directory']['Output'], 'tag', tag_name, 'index.html')
            struct = content_path(content, path)
            list.append(struct)
        return list