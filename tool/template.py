import tool.utils as utils
import tool.module as module
from tool.config import config

class _Template():
    def __init__(self):
        template_path = utils.join_path(config.template_path, 'template.html')
        template_str = utils.html_open(template_path)

        list_nav = module.nav_module()
        template_str = template_str.replace('{&Nav_module&}', str(list_nav))
        self.template_str = template_str.replace('{@Base@}', config.site_prefix)
        
    def page(self):
        self.style = "page"
        path = utils.join_path(config.template_path, self.style + '.html')
        content = utils.html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))
    
    def post(self):
        self.style = "post"
        path = utils.join_path(config.template_path, self.style + '.html')
        content = utils.html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))
    
    def home(self):
        self.style = "home"
        path = utils.join_path(config.template_path, self.style + '.html')
        content = utils.html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))

    def archive(self):
        self.style = "archive"
        path = utils.join_path(config.template_path, self.style + '.html')
        content = utils.html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))

    def category(self):
        self.style = "category"
        path = utils.join_path(config.template_path, self.style + '.html')
        content = utils.html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))

    def tag(self):
        self.style = "tag"
        path = utils.join_path(config.template_path, self.style + '.html')
        content = utils.html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))

    def replace(self, placeholder, string):
        if placeholder in self.template_str:
            self.template_str = self.template_str.replace(placeholder, string)

    def str(self):
        return self.template_str
