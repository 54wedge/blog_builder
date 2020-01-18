import re
import time
import os
import shutil
import yaml
import maya
import pathlib

def get_name_index(path):
    if is_dir(path):
        return path.split('/')[-1]
    elif is_file(path):
        return path.split('/')[-2]

def get_name(path):
    try:
        name_index = get_name_index(path)
        pattern = '(.+)\_(\d+)'
        m = re.search(pattern,name_index)
        name = m.group(1)
    except AttributeError:
        name = name = path.split('/')[-1]
        name = name[0:-5]         #remove .html
    return name

def get_index(path):
    name_index = get_name_index(path)
    pattern = '(.+)\_(\d+)'
    m = re.search(pattern,name_index)
    index = m.group(2)
    return index

def get_time(path,option = None):
    if option == 'modify':
        return os.path.getmtime(path)
    elif option == 'create':
        return os.path.getctime(path)
    else:
        raise TypeError('option for get_time() is missing or incorrect')

def get_config(section,item = ''):
    with open('config.yml','r') as config:
        config = yaml.safe_load(config)
    if item:
        return config[section][item]
    else:
        return config[section]

def append_html(path):
    new_path = os.path.join(path,'index.html')
    return new_path

def remove_page_index(path):
    new_path = path.replace(get_name_index(path),get_name(path))
    return new_path

def in_to_out(path):
    new_path = path.replace(get_config('Directory','Input'),get_config('Directory','Output'))
    return new_path

def relative_path(path):
    #new_path = path.replace(get_config('Directory','Input'),get_config('Site','Prefix'))
    new_path = path.replace(get_config('Directory','Output'),'../')
    return new_path

def get_list(option = None):
    if option == 'post':
        path = get_config('Directory','Post')
        post_names = os.listdir(path)
        list = []
        for i in post_names:
            full_path = os.path.join(path,i)
            if is_file(full_path):
                if(i.split('.')[-1] == 'html'):
                    list.append(full_path)
        #list = sorted(list,key = lambda i:get_time(i,'modify'))
        return(list)
    elif option == 'page':
        path = get_config('Directory','Input')
        pattern = '(.+)_(\d+)'
        dir_names = os.listdir(path)
        list = []
        for i in dir_names:
            full_path = os.path.join(path,i)
            if is_dir(full_path):
                if re.search(pattern,full_path):
                    list.append(full_path)
        list = sorted(list,key = lambda i:get_index(i))
        return list
    else:
        raise TypeError('option for get_list() is missing or incorrect')

def is_file(path):      ##Rewrite
    if os.path.exists(path):
        if os.path.isfile(path):
            return True
        else:
            return False
    elif path.split('.')[-1] == 'html':
        return True
    else:
        return False

def is_dir(path):        ##Rewrite
    if os.path.exists(path):
        if os.path.isdir(path):
            return True
        else:
            return False
    else:
        end = path.split('/')[-1]
        if end == end.split('.')[-1]:
            return True
        else:
            return False

def is_page_ignore(path):
    if is_dir(path):
        for i in get_config('Ignore'):
            if get_name(path).lower() == i.lower():
                return True
    else:
        return None

def check_path(path):
    if is_dir(path):
        if os.path.exists(path):
            return True
        else:
            #print(path)
            os.makedirs(path)
    elif is_file(path):
        new_path = path.rsplit('/',1)[0]
        if os.path.exists(new_path):
            return True
        else:
            #print(new_path)
            os.makedirs(new_path)

def initial():
    shutil.rmtree(get_config('Directory','Output'))
    check_path(get_config('Directory','Output'))
    post_path = in_to_out(get_config('Directory','Post'))
    check_path(post_path)
    asset_path = get_config('Directory','Asset')
    shutil.copytree(get_config('Directory','Asset'),get_config('Directory','Output')+'asset/')
    page_list = get_list('page')
    for page in page_list:
        page = in_to_out(page)
        page = remove_page_index(page)
        check_path(page)
