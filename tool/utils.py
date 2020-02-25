import os
import shutil
import yaml
from pathlib import Path as _Path
import htmlmin
from bs4 import BeautifulSoup as bs

def style(string, *args):
    style_dict = {'reset':'\033[00m', 'bold':'\033[01m', 'disable':'\033[02m',
        'underline':'\033[04m', 'reverse':'\033[07m', 'strikethrough':'\033[09m',
        'invisible':'\033[08m', 'black':'\033[30m', 'red':'\033[31m',
        'green':'\033[32m', 'orange':'\033[33m', 'blue':'\033[34m',
        'purple':'\033[35m', 'cyan':'\033[36m', 'lightgrey':'\033[37m',
        'darkgrey':'\033[90m', 'lightred':'\033[91m', 'lightgreen':'\033[92m',
        'yellow':'\033[93m', 'lightblue':'\033[94m', 'pink':'\033[95m',
        'lightcyan':'\033[96m'}
    for arg in args:
        string = style_dict[arg] + string
    return string + style_dict['reset']

with open('config.yml','r') as config:
    config = yaml.safe_load(config)

def get_time(path,option = None):
    if option == 'modify':
        return os.path.getmtime(path)
    elif option == 'create':
        return os.path.getctime(path)
    else:
        raise TypeError('option for get_time() is missing or incorrect')

def join_path(path, *args):
    for arg in args:
        path = os.path.join(path,arg)
    return path

def get_list(option = None):
    if option == 'post':
        path = os.path.join(config['Directory']['Output'], 'post')
        post_names = os.listdir(path)
        list = []
        for i in post_names:
            full_path = os.path.join(path,i)
            if full_path.split('.')[-1] == 'html':
                list.append(full_path)
        return(list)
    elif option == 'page':
        path = config['Directory']['Output']
        page_list = config['Page']
        list = []
        for page_name in page_list:
            if page_name[0] is '_':
                continue
            full_path = os.path.join(path,page_name)
            full_path = os.path.join(full_path,'index.html')
            if os.path.exists(full_path):
                list.append(full_path)
            else:
                print(style(' !!Page ' + full_path + ' does not exist', 'red','bold'))
        return list
    else:
        raise TypeError('option for get_list() is missing or incorrect')

def check_parent_path(path):
    if path.split('.')[-1] == 'html':
        new_path = path.rsplit('/',1)[0]
        if os.path.exists(new_path):
            return True
        else:
            os.makedirs(new_path)
    else:
        if os.path.exists(path):
            return True
        else:
            os.makedirs(path)

def initial():
    if os.path.exists(config['Directory']['Output']):
        shutil.rmtree(config['Directory']['Output'])
    shutil.copytree(config['Directory']['Input'], config['Directory']['Output'], ignore=shutil.ignore_patterns('*.md', '*.txt', '*_ignore*', '.DS_Store'))
    asset_path = os.path.join(config['Directory']['Template'], 'asset')
    shutil.copytree(asset_path,os.path.join(config['Directory']['Output'], 'asset'),  ignore=shutil.ignore_patterns('*.md', '*.txt', '.DS_Store'))

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
    if option == 'str':
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
    else:
        raise TypeError('option for safe_save() is missing or incorrect')

def str_to_bs(html):
    soup = bs(html,'lxml')
    return soup

empty_soup = bs('','lxml')

def a_href(name,path):
    new_a = empty_soup.new_tag('a',href = path)
    new_a.string = name
    return new_a
