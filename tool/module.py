import tool.utils as utils
from tool.utils import config
from itertools import groupby
import maya

def archive_module(post_list):
    if config['Site']['Archive_group_by'] == 'month':
        style_key = '%B %Y'
    elif config['Site']['Archive_group_by'] == 'year':
        style_key = '%Y'
    new_div = utils.empty_soup.new_tag('div')
    for key,group in groupby(post_list, key = lambda i:i.meta.maya.datetime().strftime(style_key)):
        new_h2 = utils.empty_soup.new_tag('h2')
        new_h2.string = key
        new_div.append(new_h2)
        new_ul = utils.empty_soup.new_tag('ul')
        for post in list(group):
            new_a = post.link
            new_li = utils.empty_soup.new_tag('li')
            new_li.append(new_a)
            new_ul.append(new_li)
        new_div.append(new_ul)
    return new_div

def post_module(post_list):
    new_div = utils.empty_soup.new_tag('div')
    new_ul = utils.empty_soup.new_tag('ul')
    for post in post_list:
        new_a = post.link
        new_li = utils.empty_soup.new_tag('li')
        new_li.append(new_a)
        new_ul.append(new_li)
    new_div.append(new_ul)
    return new_div

def home_module(post_list):
    new_div = utils.empty_soup.new_tag('div')
    new_ul = utils.empty_soup.new_tag('ul')
    for post in post_list:
        new_a = post.link
        new_li = utils.empty_soup.new_tag('li')
        new_div_2 = utils.empty_soup.new_tag('div')
        new_div_2.string = get_abstract(post)
        new_li.append(new_a)
        new_li.append(new_div_2)
        new_ul.append(new_li)
        new_div.append(new_ul)
    return new_div

def nav_module():
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
