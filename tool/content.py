import tool.utils as utils
from tool.meta import _Meta
import tool.module as module
import os
import tool.utils as utils

def read_source(type = None):
    path_list = utils.get_list(type)
    content_list = []
    for path in path_list:
        content = _Content(path, type)
        content_list.append(content)
    content_list.sort(key = lambda i:i.meta.date_epoch, reverse = True)
    return content_list

class _Content:
    def __init__(self, path, template):
        self.path = path
        self.template = template
        self.type = template.style
        self.meta = _Meta(path)
        self.link = utils.a_href(self.meta.title, \
                                 os.path.join("..", path.split("/")[-2], path.split("/")[-1]))
        self.content = self.build()
        self.template.reset()

    def build(self):
        self.template.replace('{@Page_Title@}', self.meta.title)
        self.template.replace('{&Body&}',str(self.meta.body))
        for key in self.meta.dict:
            if key == 'Category':
                if self.type == 'page':
                    pass
                else:
                    category_path = utils.join_path('../category', self.meta.category, 'index.html')
                    category_link = utils.a_href(self.meta.category,category_path)
                    self.template.replace('{&'+key+'&}', str(category_link))
            elif key == 'Tag':
                if self.type == 'page':
                    pass
                else:
                    span_tag = module.tag_span(self.meta.tag)
                    self.template.replace('{&'+key+'&}', str(span_tag))
            else:
                self.template.replace('{@'+key+'@}', self.meta.dict[key])
        return self.template.str()