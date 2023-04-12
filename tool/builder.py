from tool.content import _Content
from tool.router import _Router
import tool.utils as utils
import sys
import os
import yaml
import shutil


class _Builder:
    def __init__(self, path):
        self.root = path
        self.config = self.set_config(path)
        self.output_path = self.config['Directory']['Output']
        self.input_path = self.config['Directory']['Input']
        self.template_path = self.config['Directory']['Template']
        self.initial()
        self.page_list = self.set_content_list(type = 'page')
        self.post_list = self.set_content_list(type = 'post')
        self.router = _Router(self.config, self.post_list)

    def initial(self):
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)
        shutil.copytree(self.input_path, self.output_path, \
                        ignore=shutil.ignore_patterns('*.md', '*.txt', '*_ignore*', '.DS_Store'))
        asset_path = os.path.join(self.template_path, 'asset')
        shutil.copytree(asset_path,os.path.join(self.output_path, 'asset'),  \
                        ignore=shutil.ignore_patterns('*.md', '*.txt', '.DS_Store'))

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
        print('Building router......')
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

    def set_content_list(self, type = None):
        path_list = self.content_list(type)
        content_list = []
        for path in path_list:
            content = _Content(self.config, path, type)
            content_list.append(content)
        content_list.sort(key = lambda i:i.meta.date_epoch, reverse = True)
        return content_list
    
    def set_config(self, path):
        if "-c" in sys.argv:
            config_path = sys.argv[sys.argv.index("-c")+1]
        else:
            config_path = os.path.join(path,"./config.yml")
        utils.print_style(config_path,'green')
        with open(config_path, 'r') as config:
            config = yaml.safe_load(config)
            return config
        
    def get_config(self):
        return self.config
    
    def content_list(self, option = None):
        if option == 'post':
            path = os.path.join(self.output_path, 'post')
            post_names = os.listdir(path)
            list = []
            for i in post_names:
                full_path = os.path.join(path,i)
                if full_path.split('.')[-1] == 'html':
                    list.append(full_path)
            return(list)
        elif option == 'page':
            path = self.output_path
            page_list = self.config['Page']
            list = []
            for page_name in page_list:
                if page_name[0] == '_':
                    continue
                full_path = os.path.join(path,page_name)
                full_path = os.path.join(full_path,'index.html')
                if os.path.exists(full_path):
                    list.append(full_path)
                else:
                    print(utils.print_style(' !!Page ' + full_path + ' does not exist', 'red','bold'))
            return list
        else:
            raise TypeError('option for get_list() is missing or incorrect')