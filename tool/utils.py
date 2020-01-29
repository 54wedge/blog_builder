import os
import shutil
import yaml
from pathlib import Path as _Path
import htmlmin
from bs4 import BeautifulSoup as bs

with open('config.yml','r') as config:
    config = yaml.safe_load(config)

def get_time(path,option = None):
    if option == 'modify':
        return os.path.getmtime(path)
    elif option == 'create':
        return os.path.getctime(path)
    else:
        raise TypeError('option for get_time() is missing or incorrect')

def get_config(section,item = ''):
    if item:
        return config[section][item]
    else:
        return config[section]

def in_to_out(path):
    new_path = path.replace(get_config('Directory','Input'),get_config('Directory','Output'))
    return new_path

def relative_path(path):
    new_path = path.replace(get_config('Directory','Output'),'../')
    return new_path

def get_list(option = None):
    if option == 'post':
        path = get_config('Directory','Post')
        post_names = os.listdir(path)
        list = []
        for i in post_names:
            full_path = os.path.join(path,i)
            if is_html(full_path):
                list.append(full_path)
        return(list)
    elif option == 'page':
        path = get_config('Directory','Input')
        page_list = get_config('Page')
        list = []
        dir_names = os.listdir(path)
        for page_name in page_list:
            if page_name in dir_names:
                full_path = os.path.join(path,page_name)
                full_path = os.path.join(full_path,'index.html')
                list.append(full_path)
        return list
    else:
        raise TypeError('option for get_list() is missing or incorrect')

def is_html(path):
    if path.split('.')[-1] == 'html':
        return True
    else:
        return False

def check_parent_path(path):
    if is_html(path):
        new_path = path.rsplit('/',1)[0]
        if os.path.exists(new_path):
            return True
        else:
            os.makedirs(new_path)

def initial():
    shutil.rmtree(get_config('Directory','Output'))
    asset_path = get_config('Directory','Asset')
    shutil.copytree(get_config('Directory','Asset'),get_config('Directory','Output')+'asset/')

def html_open(path,option = None):
    with open(path,'r') as html:
        html = html.read()
    if option is None:
        return html
    elif option == 'minify':
        mini_html = htmlmin.minify(html)
        return mini_html
    elif option == 'soup':
        soup = bs(html,'lxml')
        return soup

def safe_save(html,path,option = None):
    check_parent_path(path)
    if type(html) is bs:
        html = str(html)
    if option is None:
        with open(path,'w') as output:
            output.write(html)
    elif option == 'minify':
        mini_html = htmlmin.minify(html)
        with open(path,'w') as output:
            output.write(mini_html)
    elif option == 'prettify':
        soup = bs(html,'lxml')
        with open(path,'w') as output:
            output.write(soup.prettify())

def str_to_bs(html):
    soup = bs(html,'lxml')
    return soup

def a_href(name,path):
    soup = bs('','lxml')
    new_a = soup.new_tag('a',href = path)
    new_a.string = name
    return new_a
