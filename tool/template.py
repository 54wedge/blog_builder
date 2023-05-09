from tool.module import nav_module
from tool.config import config
from os import path as ospath

class _Template():
    def __init__(self):
        template_path = ospath.join(config.template_path, 'template.html')
        with open(template_path,'r') as html:
            self.template_str = html.read()

        list_nav = nav_module()
        self.template_str = self.template_str.replace('{&Nav_module&}', str(list_nav))
        self.template_str = self.template_str.replace('{@Base@}', config.site_prefix)
        
    def page(self):
        self.style = "page"
        path = ospath.join(config.template_path, self.style + '.html')
        with open(path,'r') as html:
            content = html.read()
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        self.template_str_old = self.template_str
    
    def post(self):
        self.style = "post"
        path = ospath.join(config.template_path, self.style + '.html')
        with open(path,'r') as html:
            content = html.read()
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        self.template_str_old = self.template_str

    def home(self):
        self.style = "home"
        path = ospath.join(config.template_path, self.style + '.html')
        with open(path,'r') as html:
            content = html.read()
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        # self.template_str_old = self.template_str

    def archive(self):
        self.style = "archive"
        path = ospath.join(config.template_path, self.style + '.html')
        with open(path,'r') as html:
            content = html.read()
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        # self.template_str_old = self.template_str

    def category(self):
        self.style = "category"
        path = ospath.join(config.template_path, self.style + '.html')
        with open(path,'r') as html:
            content = html.read()
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        self.template_str_old = self.template_str

    def tag(self):
        self.style = "tag"
        path = ospath.join(config.template_path, self.style + '.html')
        with open(path,'r') as html:
            content = html.read()
        self.template_str = self.template_str.replace('{&Content&}',str(content))
        self.template_str_old = self.template_str

    def replace(self, placeholder, string):
        if placeholder in self.template_str:
            self.template_str = self.template_str.replace(placeholder, string)

    def str(self):
        return self.template_str
    
    def reset(self):
        self.template_str = self.template_str_old
        
