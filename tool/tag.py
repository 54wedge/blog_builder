import tool.utils as utils
from tool.template import _Template


class _Tag:
    def __init__(self,tag_name,tag_list):
        self.tag_list = tag_list
        self.tag_name = tag_name
        self.path_out = utils.join_path(utils.get_config('Directory','Output'), 'tag', self.tag_name, 'index.html')

    def build(self):
        new_div = utils.empty_soup.new_tag('div')
        new_ul = utils.empty_soup.new_tag('ul')
        for post in self.tag_list:
            new_a = post.link
            new_li = utils.empty_soup.new_tag('li')
            new_li.append(new_a)
            new_ul.append(new_li)
        new_div.append(new_ul)
        new_title = utils.empty_soup.new_tag('title')
        new_title.string = '#' + self.tag_name
        tag_page = _Template('tag')
        tag_page.replace('%%Page_Title%%', str(new_title))
        tag_page.replace('%%Tag%%',self.tag_name)
        tag_page.replace('%%Post_list%%',str(new_div))
        tag_page.replace('../','../../')
        self.content = tag_page

    def print(self):
        self.build()
        return self.content.print()
