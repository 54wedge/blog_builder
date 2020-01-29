import tool.utils as utils
from tool.template import _Template


class _Tag:
    def __init__(self,tag_name,tag_list):
        self.tag_list = tag_list
        self.tag_name = tag_name
        self.path_out = utils.get_config('Directory','Output') + 'tag/' + self.tag_name + '/index.html'

    def build(self):
        soup = utils.str_to_bs('')
        new_div = soup.new_tag('div')
        new_ul = soup.new_tag('ul')
        for post in self.tag_list:
            new_a = post.link
            new_li = soup.new_tag('li')
            new_li.append(new_a)
            new_ul.append(new_li)
        new_div.append(new_ul)
        tag_page = _Template('tag').print()
        ## need edit html <title>
        tag_page = tag_page.replace('%%Tag%%',self.tag_name)
        tag_page = tag_page.replace('%%Post_list%%',str(new_div))
        self.content = tag_page.replace('../','../../')

    def print(self):
        self.build()
        return self.content
