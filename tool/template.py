import tool.utils as utils
import tool.module as module

class _Template():
    def __init__(self, config, type = None):
        self.config = config
        self.type = type
        self.page_name_list = config['Page']

        template_path = utils.join_path(config['Directory']['Template'], 'template.html')
        template = utils.html_open(template_path)

        list_nav = module.nav_module(self.page_name_list)
        template = template.replace('{&Nav_module&}', str(list_nav))
        template = template.replace('{$Base$}', config['Site']['Prefix'])

        if type == 'page' or 'post' or 'archive' or 'category' or 'tag' or 'home':
            path = utils.join_path(config['Directory']['Template'], self.type + '.html')
        else:
            raise TypeError('Failed to initialize _Template class. Missing or incorrect option')
        content = utils.html_open(path)
        self.template = template.replace('{&Content&}',str(content))

    def replace(self, placeholder, string):
        if placeholder in self.template:
            self.template = self.template.replace(placeholder, string)

    def str(self):
        return self.template
