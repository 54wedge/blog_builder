from tool.utils import join_path, html_open
from tool.module import nav_module
from tool.config import config

class _Template():
    def __init__(self):
        template_path = join_path(config.template_path, 'template.html')
        template_str = html_open(template_path)

        list_nav = nav_module()
        template_str = template_str.replace('{&Nav_module&}', str(list_nav))
        self.template_str = template_str.replace('{@Base@}', config.site_prefix)
        
    def page(self):
        self.style = "page"
        path = join_path(config.template_path, self.style + '.html')
        content = html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        self.template_str_old = self.template_str
    
    def post(self):
        self.style = "post"
        path = join_path(config.template_path, self.style + '.html')
        content = html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        self.template_str_old = self.template_str

    def home(self):
        self.style = "home"
        path = join_path(config.template_path, self.style + '.html')
        content = html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        self.template_str_old = self.template_str

    def archive(self):
        self.style = "archive"
        path = join_path(config.template_path, self.style + '.html')
        content = html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        self.template_str_old = self.template_str

    def category(self):
        self.style = "category"
        path = join_path(config.template_path, self.style + '.html')
        content = html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        self.template_str_old = self.template_str

    def tag(self):
        self.style = "tag"
        path = join_path(config.template_path, self.style + '.html')
        content = html_open(path)
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        self.template_str_old = self.template_str

    def replace(self, placeholder, string):
        if placeholder in self.template_str:
            self.template_str = self.template_str.replace(placeholder, string)

    def str(self):
        return self.template_str
    
    def reset(self):
        self.template_str = self.template_str_old
        
