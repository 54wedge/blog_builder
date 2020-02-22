import tool.utils as utils

template_path = utils.get_config('Directory','Template') + 'template.html'
template = utils.html_open(template_path)

soup = utils.str_to_bs('')
page_name_list = utils.get_config('Page')
new_nav = soup.new_tag('nav',id = 'nav-menu' )
for page_name in page_name_list:
    if page_name == '_Home':
        page_name = 'Home'
        path = '../index.html'
    elif page_name == '_Archive':
        page_name = 'Archive'
        path = '../' + page_name + '/index.html'
    else:
        path = '../' + page_name + '/index.html'
    new_a = utils.a_href(page_name,path)
    new_nav.append(new_a)
template = template.replace('%%Nav%%', str(new_nav))
new_base = soup.new_tag('base', href = utils.get_config('Site','Prefix'))
template = template.replace('%%Base%%', str(new_base))

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
            self.type = 'index.html'
        else:
            raise TypeError('Failed to initialize _Template class. Missing or incorrect option')
        content_path = utils.get_config('Directory','Template') + self.type
        self.content = utils.html_open(content_path)
        self.template = template

    def replace(self, placeholder, string):
        if placeholder in self.content:
            self.content = self.content.replace(placeholder, string)
        if placeholder in self.template:
            self.template = self.template.replace(placeholder, string)
        #else:
        #    print(utils.style(' **' + placeholder + ' is not found in template html','yellow','bold'))

    def print(self):
        self.replace('%%Content%%', self.content)
        return self.template
