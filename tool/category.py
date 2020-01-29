import tool.utils as utils
from tool.template import _Template


class _Category:
    def __init__(self,category_list):
        self.category_list = category_list
        self.category_name = self.category_list[0].meta.category
        self.path_out = utils.get_config('Directory','Output') + 'category/' + self.category_name + '/index.html'

    def build(self):
        soup = utils.str_to_bs('')
        new_div = soup.new_tag('div')
        new_ul = soup.new_tag('ul')
        for post in self.category_list:
            new_a = post.link
            new_li = soup.new_tag('li')
            new_li.append(new_a)
            new_ul.append(new_li)
        new_div.append(new_ul)
        category_page = _Template('category').print()
        ## need edit html <title>
        category_page = category_page.replace('%%Category%%',self.category_name)
        category_page = category_page.replace('%%Post_list%%',str(new_div))
        self.content = category_page.replace('../','../../')

    def print(self):
        self.build()
        return self.content
