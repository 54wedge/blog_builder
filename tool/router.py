from tool.utils import join_path
from tool.template import _Template
from tool.config import config
from tool.module import home_mini_post_list, archive_post_list, post_module

class content_path:
    def __init__(self, content, path):
        self.content = content
        self.path = path

class _Router():
    def __init__(self, post_list):
        self.post_list = post_list
        self.home_page = _Home(post_list)
        self.archive_page = _Archive(post_list)
        self.category_page_list = _Category(post_list).category_list()
        self.tag_page_list = _Tag(post_list).tag_list()

class _Home:
    def __init__(self, post_list):
        self.post_list = post_list[0:config.home_size]
        self.path = join_path(config.output_path, 'index.html')
        self.template = _Template()
        self.template.home()
        self.content = self.build()

    def build(self):
        list_home = home_mini_post_list(self.post_list)
        self.template.replace('{@Page_Title@}', config.home_page_title)
        self.template.replace('{&Home_mini_post_list&}',str(list_home))
        self.template.replace('../','./')
        return self.template.str()

class _Archive():
    def __init__(self, post_list):
        self.post_list = post_list
        self.path = join_path(config.output_path, 'Archive/index.html')
        self.template = _Template()
        self.template.archive()
        self.content = self.build()

    def build(self):
        list_archive = archive_post_list(self.post_list)
        self.template.replace('{@Page_Title@}', 'Archive')
        self.template.replace('{&Archive_post_list&}',str(list_archive))
        return self.template.str()

class _Category:
    def __init__(self, post_list):
        self.template = _Template()
        self.template.category()
        self.category_dict = {}
        for post in post_list:
            try:
                self.category_dict[post.meta.category].append(post)
            except KeyError:
                self.category_dict[post.meta.category] = []
                self.category_dict[post.meta.category].append(post)

    def replace(self, category_name):
        category_list = self.category_dict[category_name]
        list_category = post_module(category_list)
        self.template.replace('@Page_Title@}', category_name)
        self.template.replace('{@Category@}', category_name)
        self.template.replace('{&Post_module&}',str(list_category))
        self.template.replace('../','../../')
        return self.template.str()

    def category_list(self):
        category_list = []
        for category_name in self.category_dict.keys():
            content = self.replace(category_name)
            self.template.reset()
            path = join_path(config.output_path, 'category', category_name, 'index.html')
            struct = content_path(content, path)
            category_list.append(struct)
        return category_list

class _Tag:
    def __init__(self, post_list):
        self.template = _Template()
        self.template.tag()
        self.tag_dict = {}
        for post in post_list:
            for meta_tag in post.meta.tag:
                try:
                    self.tag_dict[meta_tag].append(post)
                except KeyError:
                    self.tag_dict[meta_tag] = []
                    self.tag_dict[meta_tag].append(post)

    def replace(self, tag_name):
        tag_list = self.tag_dict[tag_name]
        list_tag = post_module(tag_list)
        self.template.replace('{@Page_Title@}', '#' + tag_name)
        self.template.replace('{@Tag@}', tag_name)
        self.template.replace('{&Post_module&}',str(list_tag))
        self.template.replace('../','../../')
        return self.template.str()

    def tag_list(self):
        tag_list = []
        for tag_name in self.tag_dict.keys():
            content = self.replace(tag_name)
            self.template.reset()
            path = join_path(config.output_path, 'tag', tag_name, 'index.html')
            struct = content_path(content, path)
            tag_list.append(struct)
        return tag_list