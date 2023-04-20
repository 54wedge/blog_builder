from tool.content import _Content
from tool.router import _Router
import tool.utils as utils
import sys
import os
import yaml
import shutil
from tool.config import config

class _Builder:
    def __init__(self, path):
        self.initial()
        self.page_list = self.page_list()
        self.post_list = self.post_list()
        self.router = _Router(self.post_list)

    def initial(self):
        if os.path.exists(config.output_path):
            shutil.rmtree(config.output_path)
        shutil.copytree(config.input_path, config.output_path, \
                        ignore=shutil.ignore_patterns('*.md', '*.txt', '*_ignore*', '.DS_Store'))
        asset_path = os.path.join(config.template_path, 'asset')
        shutil.copytree(asset_path,os.path.join(config.output_path, 'asset'),  \
                        ignore=shutil.ignore_patterns('*.md', '*.txt', '.DS_Store'))

    def build_page(self):
        utils.nsprint('Building pages......')
        for page in self.page_list:
            utils.safe_save(page.content, page.path)
            utils.nsprint(' --page '+ utils.sstyle(page.path,'green') + ' is built')
            # utils.nsutils.nsprint(" --page "+ page.path + " is built")

    def build_post(self):
        utils.nsprint('Building posts......')
        for post in self.post_list:
            utils.safe_save(post.content, post.path)
            utils.nsprint(' --post ' + utils.sstyle(post.path,'green') + ' is built')

    def build_router(self):
        utils.nsprint('Building router......')
        utils.safe_save(self.router.home.content, self.router.home.path)
        utils.nsprint(' --Home page ' + utils.sstyle(self.router.home.path,'green') + ' is built')
        utils.safe_save(self.router.archive.content, self.router.archive.path,)
        utils.nsprint(' --Archive page ' + utils.sstyle(self.router.archive.path,'green') + ' is built')
        for category in self.router.category_list:
            utils.safe_save(category.content, category.path)
            utils.nsprint(' --Category page ' + utils.sstyle(category.path,'green') + ' is built')
        for tag in self.router.tag_list:
            utils.safe_save(tag.content, tag.path)
            utils.nsprint(' --Tag page ' + utils.sstyle(tag.path,'green') + ' is built')
    
    def page_list(self):
        path_list = self.get_page_path_list()
        content_list = []
        for path in path_list:
            content = _Content(path, "page")
            content_list.append(content)
        content_list.sort(key = lambda i:i.meta.date_epoch, reverse = True)
        return content_list
    
    def post_list(self):
        path_list = self.get_post_path_list()
        content_list = []
        for path in path_list:
            content = _Content(path, "post")
            content_list.append(content)
        content_list.sort(key = lambda i:i.meta.date_epoch, reverse = True)
        return content_list
    
    def get_page_path_list(self):
        path = config.output_path
        page_list = config.page_name_list
        page_path_list = []
        for page_name in page_list:
            if page_name[0] == '_':
                continue
            full_path = os.path.join(path,page_name)
            full_path = os.path.join(full_path,'index.html')
            if os.path.exists(full_path):
                page_path_list.append(full_path)
            else:
                utils.nsprint(utils.sstyle(' !!Page ' + full_path + ' does not exist', 'red','bold'))
        return page_path_list

    def get_post_path_list(self):
        path = os.path.join(config.output_path, 'post')
        post_names = os.listdir(path)
        post_path_list = []
        for i in post_names:
            full_path = os.path.join(path,i)
            if full_path.split('.')[-1] == 'html':
                post_path_list.append(full_path)
        return post_path_list