import tool.utils as utils
from tool.utils import config
import tool.gen_list as gen_list

template_path = utils.join_path(config['Directory']['Template'], 'template.html')
template = utils.html_open(template_path)

list_nav = gen_list.nav()
template = template.replace('{&Nav&}', str(list_nav))
new_base = utils.empty_soup.new_tag('base', href = config['Site']['Prefix'])
template = template.replace('{&Base&}', str(new_base))

class _Template():
    def __init__(self,type = None):
        if type == 'page':
            self.type = 'page.html'
        elif type == 'post':
            self.type = 'post.html'
        elif type == 'archive':
            self.type = 'archive.html'
        elif type == 'category':
            self.type = 'category.html'
        elif type == 'tag':
            self.type = 'tag.html'
        elif type == 'home':
            self.type = 'home.html'
        else:
            raise TypeError('Failed to initialize _Template class. Missing or incorrect option')
        content_path = utils.join_path(config['Directory']['Template'], self.type)
        content = utils.html_open(content_path)
        self.template = template.replace('{&Content&}',str(content))

    def replace(self, placeholder, string):
        if placeholder in self.template:
            self.template = self.template.replace(placeholder, string)

    def print(self):
        return self.template
