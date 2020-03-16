import tool.utils as utils
from tool.template import _Template
from tool.meta import _Meta
from tool.utils import config
import tool.gen_list as gen_list


class _Content:
    def __init__(self,path,type):
        self.path = path
        self.type = type
        self.meta = _Meta(path)
        self.link = utils.a_href(self.meta.title,self.path.replace(config['Directory']['Output'],'..'))

    def build(self):
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = self.meta.title
        template = _Template(self.type)
        template.replace('{&Page_Title&}', str(new_title))
        template.replace('{&Body&}',str(self.meta.content))
        for key in self.meta.dict:
            if key == 'Category':
                category_path = utils.join_path('../category', self.meta.dict[key], 'index.html')
                category_link = utils.a_href(self.meta.dict[key],category_path)
                template.replace('{&'+key+'&}', str(category_link))
            elif key == 'Tag':
                span_tag = gen_list.tag_span(self.meta.dict['Tag'])
                template.replace('{&'+key+'&}', str(span_tag))
            else:
                template.replace('{$'+key+'$}', self.meta.dict[key])
        self.content = template
        #self.insert_meta()

    def print(self):
        self.build()
        return self.content.print()
