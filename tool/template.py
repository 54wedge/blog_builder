import tool.utils as utils


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
        elif type == 'index':
            self.type = 'index.html'
        else:
            raise TypeError('Failed to initialize _Template class. Missing or incorrect option')
        path_header = utils.get_config('Directory','Template') + 'header.html'
        path_footer = utils.get_config('Directory','Template') + 'footer.html'
        path = utils.get_config('Directory','Template') + self.type
        self.content = utils.html_open(path_header) + utils.html_open(path) + utils.html_open(path_footer)
        soup = utils.str_to_bs('')
        new_base = soup.new_tag('base', href = utils.get_config('Site','Prefix'))
        self.content = self.content.replace('%%Base%%', str(new_base))

    def build(self):
        soup = utils.str_to_bs('')
        page_name_list = utils.get_config('Page')
        page_name_list[:] = [page_name.replace('_','') for page_name in page_name_list]
        #print(page_name_list)
        new_nav = soup.new_tag('nav',id = 'nav-menu' )
        soup.append(new_nav)
        for page_name in page_name_list:
            if page_name == 'Home':
                path = '../index.html'
            else:
                path = '../' + page_name + '/index.html'
            new_a = utils.a_href(page_name,path)
            soup.nav.append(new_a)
        self.content = self.content.replace('%%Nav%%',str(soup))

    def print(self):
        self.build()
        return self.content
