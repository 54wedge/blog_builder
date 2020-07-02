import tool.utils as utils
from tool.template import _Template
from tool.meta import _Meta
from tool.utils import config
import tool.module as module

def read_source(type = None):
    path_list = utils.get_list(type)
    content_list = []
    for path in path_list:
        content = _Content(path, type)
        content_list.append(content)
    content_list.sort(key = lambda i:i.meta.date_epoch, reverse = True)
    return content_list

class _Content:
    def __init__(self,path,type):
        self.path = path
        self.type = type
        self.meta = _Meta(path)
        self.link = utils.a_href(self.meta.title,self.path.replace(config['Directory']['Output'],'..'))
        self.content = self.build()

    def build(self):
        template = _Template(self.type)
        template.replace('{$Page_Title$}', self.meta.title)
        template.replace('{&Body&}',str(self.meta.body))
        for key in self.meta.dict:
            if key == 'Category':
                if self.type == 'page':
                    pass
                else:
                    category_path = utils.join_path('../category', self.meta.dict[key], 'index.html')
                    category_link = utils.a_href(self.meta.dict[key],category_path)
                    template.replace('{&'+key+'&}', str(category_link))
            elif key == 'Tag':
                if self.type == 'page':
                    pass
                else:
                    span_tag = module.tag_span(self.meta.dict['Tag'])
                    template.replace('{&'+key+'&}', str(span_tag))
            else:
                template.replace('{$'+key+'$}', self.meta.dict[key])
        return template.str()
