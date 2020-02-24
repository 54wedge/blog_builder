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

def get_config(section,item = ''):
    if item:
        return config[section][item]
    else:
        return config[section]

def in_to_out(path):
    new_path = path.replace(get_config('Directory','Input'),get_config('Directory','Output'))
    return new_path

def relative_path(path):
    new_path = path.replace(get_config('Directory','Output'),'..')
    return new_path

def join_path(path, *args):
    for arg in args:
        path = os.path.join(path,arg)
    return path

def get_list(option = None):
    if option == 'post':
        path = os.path.join(get_config('Directory','Input'), 'post')
        post_names = os.listdir(path)
        list = []
        for i in post_names:
            full_path = os.path.join(path,i)
            if full_path.split('.')[-1] == 'html':
                list.append(full_path)
        return(list)
    elif option == 'page':
        path = get_config('Directory','Input')
        page_list = get_config('Page')
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
    if os.path.exists(get_config('Directory','Output')):
        shutil.rmtree(get_config('Directory','Output'))
    shutil.copytree(get_config('Directory','Input'), get_config('Directory','Output'), ignore=shutil.ignore_patterns('*.md', '*.txt'))
    asset_path = os.path.join(get_config('Directory','Template'), 'asset')
    shutil.copytree(asset_path,os.path.join(get_config('Directory','Output'), 'asset'))

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

empty_soup = str_to_bs('')

def a_href(name,path):
    soup = bs('','lxml')
    new_a = soup.new_tag('a',href = path)
    new_a.string = name
    return new_a
