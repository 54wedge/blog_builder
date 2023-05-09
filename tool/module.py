from tool.meta import empty_soup, str_to_bs
from itertools import groupby
from tool.config import config
from os import path as ospath

def archive_post_list(post_path_list):
    if config.archive_group == 'month':
        style_key = '%B %Y'
    elif config.archive_group == 'year':
        style_key = '%Y'
    new_div = empty_soup.new_tag('div')
    if post_path_list == []:
        new_p = empty_soup.new_tag('ul')
        new_p.string = "There is no post"
        new_div.append(new_p)
    elif config.archive_group == "none":
        new_ul = empty_soup.new_tag('ul')
        for post in post_path_list:
            new_a = post.link
            new_li = empty_soup.new_tag('li')
            new_li.append(new_a)
            new_ul.append(new_li)
        new_div.append(new_ul)
    else:
        for key,group in groupby(post_path_list, key = lambda i:i.meta.datetime.strftime(style_key)):
            new_h2 = empty_soup.new_tag('h2')
            new_h2.string = key
            new_div.append(new_h2)
            new_ul = empty_soup.new_tag('ul')
            for post in list(group):
                new_a = post.link
                new_li = empty_soup.new_tag('li')
                new_li.append(new_a)
                new_ul.append(new_li)
            new_div.append(new_ul)
    return new_div

def post_module(post_list):
    new_div = empty_soup.new_tag('div')
    new_ul = empty_soup.new_tag('ul')
    for post in post_list:
        new_a = post.link
        new_li = empty_soup.new_tag('li')
        new_li.append(new_a)
        new_ul.append(new_li)
    new_div.append(new_ul)
    return new_div

def home_mini_post_list(post_path_list):
    new_div = empty_soup.new_tag('div')
    
    if post_path_list == []:
        new_p = empty_soup.new_tag('ul')
        new_p.string = "There is no post"
        new_div.append(new_p)
    else:
        for post_path in post_path_list:
            new_a = post_path.link
            new_ul = empty_soup.new_tag('ul')
            new_li = empty_soup.new_tag('li')
            new_div1 = empty_soup.new_tag('div')
            new_div1.string = get_abstract(post_path)
            new_li.append(new_a)
            new_li.append(new_div1)
            new_ul.append(new_li)
            new_div.append(new_ul)
    return new_div

def nav_module():
    new_nav = empty_soup.new_tag('nav',id = 'nav-menu' )
    for page_name in config.page_name_list:
        if page_name == '_Home':
            page_name = 'Home'
            path = '../index.html'
        elif page_name == '_Archive':
            page_name = 'Archive'
            path = ospath.join('../', page_name, 'index.html')
        else:
            path = ospath.join('../', page_name, 'index.html')
        new_a = empty_soup.new_tag('a',href = path)
        new_a.string = page_name
        new_nav.append(new_a)
    return new_nav

def tag_span(tag_list):
    new_span = empty_soup.new_tag('span',id = 'tag')
    for tag in tag_list:
        tag_path = ospath.join('../tag', tag, 'index.html')
        tag_link = empty_soup.new_tag('a',href = tag_path)
        tag_link.string = '#' + tag
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
            abstract = str_to_bs(abstract)
            abstract = abstract.get_text()
        else:
            abstract = 'No abstract provided'
    return abstract
