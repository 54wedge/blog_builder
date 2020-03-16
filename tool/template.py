import tool.utils as utils
from tool.utils import config

template_path = utils.join_path(config['Directory']['Template'], 'template.html')
template = utils.html_open(template_path)

page_name_list = config['Page']
new_nav = utils.empty_soup.new_tag('nav',id = 'nav-menu' )
for page_name in page_name_list:
    if page_name == '_Home':
        page_name = 'Home'
        path = '../index.html'
    elif page_name == '_Archive':
        page_name = 'Archive'
        path = utils.join_path('../', page_name, 'index.html')
    else:
        path = utils.join_path('../', page_name, 'index.html')
    new_a = utils.a_href(page_name,path)
    new_nav.append(new_a)
template = template.replace('{&Nav&}', str(new_nav))
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
        self.content = utils.html_open(content_path)
        self.template = template

    def replace(self, placeholder, string):
        if placeholder in self.content:
            self.content = self.content.replace(placeholder, string)
        if placeholder in self.template:
            self.template = self.template.replace(placeholder, string)
        #else:
        #    print(utils.print_style(' **' + placeholder + ' is not found in template html','yellow','bold'))

    def print(self):
        self.replace('{&Content&}', self.content)
        return self.template
