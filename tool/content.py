from tool.utils import a_href, join_path
from tool.meta import _Meta
from tool.module import tag_span
from os import path as ospath

class _Content:
    def __init__(self, path, template):
        self.path = path
        self.template = template
        self.type = template.style
        self.meta = _Meta(path)
        self.link = a_href(self.meta.title, \
                                 ospath.join("..", path.split("/")[-2], path.split("/")[-1]))
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
                    category_path = join_path('../category', self.meta.category, 'index.html')
                    category_link = a_href(self.meta.category,category_path)
                    self.template.replace('{&'+key+'&}', str(category_link))
            elif key == 'Tag':
                if self.type == 'page':
                    pass
                else:
                    span_tag = tag_span(self.meta.tag)
                    self.template.replace('{&'+key+'&}', str(span_tag))
            else:
                self.template.replace('{@'+key+'@}', self.meta.dict[key])
        return self.template.str()