import tool.utils as utils
from tool.template import _Template
from tool.utils import config
from tool.utils import content_path
import tool.module as module

class _Router():
    def __init__(self,post_list):
        self.post_list = post_list
        self.home = _Home(post_list)
        self.archive = _Archive(post_list)
        self.category_list = _Category(post_list).list()
        self.tag_list = _Tag(post_list).list()

class _Home:
    def __init__(self,post_list):
        self.post_list = post_list[0:config['Home']['Page_size']]
        self.path = utils.join_path(config['Directory']['Output'], 'index.html')
        self.content = self.build()
        self.struct = content_path(self.content, self.path)

    def build(self):
        list_home = module.home_list(self.post_list)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = 'Home'
        home_page = _Template('home')
        home_page.replace('{&Page_Title&}', str(new_title))
        home_page.replace('{&Post_list&}',str(list_home))
        home_page.replace('../','./')
        return home_page.str()

class _Archive():
    def __init__(self,post_list):
        self.post_list = post_list
        self.path = utils.join_path(config['Directory']['Output'], 'Archive/index.html')
        self.content = self.build()
        self.struct = content_path(self.content, self.path)

    def build(self):
        list_archive = module.archive_list(self.post_list)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = 'Archive'
        archive_page = _Template('archive')
        archive_page.replace('{&Page_Title&}',str(new_title))
        archive_page.replace('{&Post_list&}',str(list_archive))
        return archive_page.str()

    def group_standard(self, post):
        if config['Config']['Archive_group_by'] == 'month':
            standard = post.meta.maya.datetime().strftime('%m/01/%Y')
        elif config['Config']['Archive_group_by'] == 'year':
            standard = post.meta.maya.datetime().strftime('01/01/%Y')
        return post.meta.maya.parse(standard).epoch

class _Category:
    def __init__(self,post_list):
        self.category_dict = {}
        for post in post_list:
            try:
                self.category_dict[post.meta.category].append(post)
            except KeyError:
                self.category_dict[post.meta.category] = []
                self.category_dict[post.meta.category].append(post)

    def build(self, category_list, category_name):
        list_category = module.post_list(category_list)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = category_name
        category_page = _Template('category')
        category_page.replace('{&Page_Title&}', str(new_title))
        category_page.replace('{$Category$}', category_name)
        category_page.replace('{&Post_list&}',str(list_category))
        category_page.replace('../','../../')
        return category_page.str()

    def list(self):
        list = []
        for category_name in self.category_dict.keys():
            category_list = self.category_dict[category_name]
            content = self.build(category_list, category_name)
            path = utils.join_path(config['Directory']['Output'], 'category', category_name, 'index.html')
            struct = content_path(content, path)
            list.append(struct)
        return list

class _Tag:
    def __init__(self,post_list):
        self.tag_dict = {}
        for post in post_list:
            for meta_tag in post.meta.tag:
                try:
                    self.tag_dict[meta_tag].append(post)
                except KeyError:
                    self.tag_dict[meta_tag] = []
                    self.tag_dict[meta_tag].append(post)

    def build(self, tag_list, tag_name):
        list_tag = module.post_list(tag_list)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = '#' + tag_name
        tag_page = _Template('tag')
        tag_page.replace('{&Page_Title&}', str(new_title))
        tag_page.replace('{$Tag$}', tag_name)
        tag_page.replace('{&Post_list&}',str(list_tag))
        tag_page.replace('../','../../')
        return tag_page.str()

    def list(self):
        list = []
        for tag_name in self.tag_dict.keys():
            tag_list = self.tag_dict[tag_name]
            content = self.build(tag_list, tag_name)
            path = utils.join_path(config['Directory']['Output'], 'tag', tag_name, 'index.html')
            struct = content_path(content, path)
            list.append(struct)
        return list
