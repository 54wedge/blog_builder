import tool.utils as utils
from tool.template import _Template
from tool.meta import _Meta
from tool.utils import config


class _Page:
    def __init__(self,path):
        self.path = path
        self.type = 'page'
        html_soup = utils.html_open(path,'soup')
        try:
            raw_meta = html_soup.find_all('code',class_ = 'meta')[0].get_text()
            if config['Config']['Hide_meta']:
                html_soup.find_all('code',class_ = 'meta')[0].parent.decompose()
        except IndexError:      #no meta data found
            print(utils.style(' **No raw meta found in ' + path, 'yellow', 'bold'))
            raw_meta = ''
        self.content_soup = html_soup.body
        self.meta = _Meta(raw_meta,path)
        try:
            self.content_soup.h1.decompose()
        except AttributeError:
            pass
        self.link = utils.a_href(self.meta.title,self.path.replace(config['Directory']['Output'],'..'))

    def build(self):
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = self.meta.title
        template = _Template(self.type)
        template.replace('%%Page_Title%%', str(new_title))
        template.replace('%%Body%%',str(self.content_soup))
        for key in self.meta.dict:
            if key == 'Category':
                category_path = utils.join_path('../category', self.meta.dict[key], 'index.html')
                category_link = utils.a_href(self.meta.dict[key],category_path)
                template.replace('%%'+key+'%%', str(category_link))
            elif key == 'Tag':
                new_span = utils.empty_soup.new_tag('span',id = 'tag')
                for tag in self.meta.dict['Tag']:
                    tag_path = utils.join_path('../tag', tag, 'index.html')
                    tag_link = utils.a_href('#' + tag,tag_path)
                    new_span.append(tag_link)
                template.replace('%%'+key+'%%', str(new_span))
            else:
                template.replace('%%'+key+'%%', self.meta.dict[key])
        self.content = template
        #self.insert_meta()

    def print(self):
        self.build()
        return self.content.print()
