from tool.content import _Content
from tool.router import _Router
from tool.template import _Template
from tool.utils import nsprint, sstyle
from os import path as ospath
from os import listdir, makedirs
from shutil import rmtree, copytree, ignore_patterns
from tool.config import config

class _Builder:
    def __init__(self, path):
        self.initial()
        self.page_list = self.page_list()
        self.post_list = self.post_list()
        self.router = _Router(self.post_list)

    def initial(self):
        if ospath.exists(config.output_path):
            rmtree(config.output_path)
        copytree(config.input_path, config.output_path, \
                        ignore=ignore_patterns('*.md', '*.txt', '*_ignore*', '.DS_Store'))
        asset_path = ospath.join(config.template_path, 'asset')
        copytree(asset_path, ospath.join(config.output_path, 'asset'),  \
                        ignore=ignore_patterns('*.md', '*.txt', '.DS_Store'))

    def build_page(self):
        nsprint('Building pages......')
        for page in self.page_list:
            self.save_html(page.content, page.path)
            nsprint(' --page '+ sstyle(page.path,'green') + ' is built')

    def build_post(self):
        nsprint('Building posts......')
        for post in self.post_list:
            self.save_html(post.content, post.path)
            nsprint(' --post ' + sstyle(post.path,'green') + ' is built')

    def build_router(self):
        nsprint('Building router......')
        self.save_html(self.router.home_page.content, self.router.home_page.path)
        nsprint(' --Home page ' + sstyle(self.router.home_page.path,'green') + ' is built')
        self.save_html(self.router.archive_page.content, self.router.archive_page.path,)
        nsprint(' --Archive page ' + sstyle(self.router.archive_page.path,'green') + ' is built')
        for category_page in self.router.category_page_list:
            self.save_html(category_page.content, category_page.path)
            nsprint(' --Category page ' + sstyle(category_page.path,'green') + ' is built')
        for tag_page in self.router.tag_page_list:
            self.save_html(tag_page.content, tag_page.path)
            nsprint(' --Tag page ' + sstyle(tag_page.path,'green') + ' is built')
    
    def page_list(self):
        path_list = self.get_page_path_list()
        template = _Template()
        template.page()
        content_list = []
        for path in path_list:
            content = _Content(path, template)
            content_list.append(content)
        content_list.sort(key = lambda i:i.meta.datetime_epoch, reverse = True)
        return content_list
    
    def post_list(self):
        path_list = self.get_post_path_list()
        template = _Template()
        template.post()
        content_list = []
        for path in path_list:
            content = _Content(path, template)
            content_list.append(content)
        content_list.sort(key = lambda i:i.meta.datetime_epoch, reverse = True)
        return content_list
    
    def get_page_path_list(self):
        path = config.output_path
        page_list = config.page_name_list
        page_path_list = []
        for page_name in page_list:
            if page_name[0] == '_':
                continue
            full_path = ospath.join(path,page_name)
            full_path = ospath.join(full_path,'index.html')
            if ospath.exists(full_path):
                page_path_list.append(full_path)
            else:
                nsprint(sstyle(' !!Page ' + full_path + ' does not exist', 'red','bold'))
        return page_path_list

    def get_post_path_list(self):
        path = ospath.join(config.output_path, 'post')
        post_names = listdir(path)
        post_path_list = []
        for i in post_names:
            full_path = ospath.join(path,i)
            if full_path.split('.')[-1] == 'html':
                post_path_list.append(full_path)
        return post_path_list
    
    def save_html(self, html, path):
        dir_path = path.rsplit('/',1)[0]
        if not ospath.exists(dir_path):
            makedirs(dir_path)
        with open(path,'w') as output:
            output.write(html)