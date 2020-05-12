import tool.utils as utils
from tool.utils import config
from itertools import groupby
import maya


def archive_list(post_list):
    month_group = []
    for key,group in groupby(post_list, key = lambda i:group_standard(i)):
        month_group.append(list(group))

    new_div = utils.empty_soup.new_tag('div')
    for month in month_group:
        new_h2 = utils.empty_soup.new_tag('h2')
        if config['Config']['Archive_group_by'] == 'month':
            new_h2.string = str(month[0].meta.maya.datetime().strftime('%B %Y'))
        elif config['Config']['Archive_group_by'] == 'year':
            new_h2.string = str(month[0].meta.maya.datetime().strftime('%Y'))
        new_div.append(new_h2)
        new_ul = utils.empty_soup.new_tag('ul')
        for post in month:
            new_a = post.link
            new_li = utils.empty_soup.new_tag('li')
            new_li.append(new_a)
            new_ul.append(new_li)
        new_div.append(new_ul)
    return new_div

def post_list(post_list):
    new_div = utils.empty_soup.new_tag('div')
    new_ul = utils.empty_soup.new_tag('ul')
    for post in post_list:
        new_a = post.link
        new_li = utils.empty_soup.new_tag('li')
        new_li.append(new_a)
        new_ul.append(new_li)
    new_div.append(new_ul)
    return new_div

def home_list(post_list):
    new_div = utils.empty_soup.new_tag('div')
    for post in post_list:
        new_a = post.link
        new_ul = utils.empty_soup.new_tag('ul')
        new_li = utils.empty_soup.new_tag('li')
        new_li.append(new_a)
        new_div_2 = utils.empty_soup.new_tag('div')
        new_div_2.string = get_abstract(post)
        new_li.append(new_a)
        new_li.append(new_div_2)
        new_ul.append(new_li)
        new_div.append(new_ul)
    return new_div

def nav_list():
    page_name_list = config['Page']
    new_nav = utils.empty_soup.new_tag('nav',id = 'nav-menu' )
    for page_name in page_name_list:
        if page_name == '_Home':
            page_name = 'Home'
            path = '../index.html'
        elif page_name == '_Archive':
            page_name = 'Archive'
            path = utils.join_path('../', page_name, 'index.html')
        else:
            path = utils.join_path('../', page_name, 'index.html')
        new_a = utils.a_href(page_name,path)
        new_nav.append(new_a)
    return new_nav

def tag_span(tag_list):
    new_span = utils.empty_soup.new_tag('span',id = 'tag')
    for tag in tag_list:
        tag_path = utils.join_path('../tag', tag, 'index.html')
        tag_link = utils.a_href('#' + tag,tag_path)
        new_span.append(tag_link)
        new_span.append(' ')
    return new_span

def group_standard(post):
    if config['Config']['Archive_group_by'] == 'month':
        standard = post.meta.maya.datetime().strftime('%m/01/%Y')
    elif config['Config']['Archive_group_by'] == 'year':
        standard = post.meta.maya.datetime().strftime('01/01/%Y')
    return maya.parse(standard).epoch

def get_abstract(post):
    try:
        abstract = post.meta.dict['Abstract']
    except KeyError:
        body = post.meta.body
        if '<!--more-->' in str(body):
            abstract = str(body).split('<!--more-->')[0]
            abstract = utils.str_to_bs(abstract)
            abstract = abstract.get_text()
        else:
            abstract = 'No abstract provided'
    return abstract
