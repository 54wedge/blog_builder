import tool.utils as utils
from tool.template import _Template


class _Home:
    def __init__(self,post_list):
        self.post_list = post_list
        self.path_out = utils.join_path(utils.get_config('Directory','Output'), 'index.html')

    def get_abstract(self,post):
        try:
            abstract = post.meta.dict['Abstract']
        except KeyError:
            body = post.content_soup
            if '<!--more-->' in str(body):
                abstract = str(body).split('<!--more-->')[0]
                abstract = utils.str_to_bs(abstract)
                abstract = abstract.get_text()
            else:
                abstract = 'No abstract provided'
        return abstract

    def build(self):
        soup = utils.str_to_bs('')
        home_page = _Template('home')
        new_div = soup.new_tag('div')
        for post in self.post_list:
            new_a = post.link
            new_ul = soup.new_tag('ul')
            new_li = soup.new_tag('li')
            new_li.append(new_a)
            new_div_2 = soup.new_tag('div')
            new_div_2.string = self.get_abstract(post)
            new_li.append(new_a)
            new_li.append(new_div_2)
            new_ul.append(new_li)
            new_div.append(new_ul)
        home_page.replace('%%Post_list%%',str(new_div))
        home_page.replace('../','./')
        self.content = home_page

    def print(self):
        self.build()
        return self.content.print()
