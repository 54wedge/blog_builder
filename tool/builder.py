import re
import time
import os
import shutil
import yaml

def get_name_index(path):
    if is_dir(path):
        return path.split('/')[-1]
    elif is_file(path):
        return path.split('/')[-2]

def get_name(path,option = None):
    if option is None:
        name_index = get_name_index(path)
        pattern = '(.+)\_(\d+)'
        m = re.search(pattern,name_index)
        name = m.group(1)
        return name
    elif option == 'html':     #for non-page
        name = path.split('/')[-1]
        name = name[0:-5]      #remove .html
        return name

def get_index(path):
    name_index = get_name_index(path)
    pattern = '(.+)\_(\d+)'
    m = re.search(pattern,name_index)
    index = m.group(2)
    return index

def get_time(path,option=''):    ##revise wait for meta support
    #print(get_config('Sort_by','Time'))
    if get_config('Time','Sort_by') == 'modify':
        #print('modify')
        if option:
            if option == 'day':
                return time.gmtime(os.path.getmtime(path)).tm_mday
            if option == 'month':
                return time.gmtime(os.path.getmtime(path)).tm_mon
            if option == 'year':
                return time.gmtime(os.path.getmtime(path)).tm_year
        else:
            return os.path.getmtime(path)
    if get_config('Time','Sort_by') == 'create':
        #print('create')
        if option:
            if option == 'day':
                return time.gmtime(os.path.getctime(path)).tm_mday
            if option == 'month':
                return time.gmtime(os.path.getctime(path)).tm_mon
            if option == 'year':
                return time.gmtime(os.path.getctime(path)).tm_year
        else:
            return os.path.getctime(path)

def get_config(section,item = ''):     ##need more test
    with open('config.yml','r') as config:
        config = yaml.safe_load(config)
    if item:
        return config[section][item]
    else:
        return config[section]

def append_html(path):      ##may not needed
    new_path = os.path.join(path,'index.html')
    return new_path

def remove_index(path):
    new_path = path.replace(get_name_index(path),get_name(path))
    return new_path

def in_to_out(path):
    new_path = path.replace(get_config('Directory','Input'),get_config('Directory','Output'))
    return new_path

def get_list(option = None):
    if option is None:
        print('need an option')
    elif option == 'post':
        path = get_config('Directory','Post')
        post_names = os.listdir(path)
        list = []
        for i in post_names:
            full_path = os.path.join(path,i)
            if is_file(full_path):
                if(i.split('.')[-1] == 'html'):
                    list.append(full_path)
        #list = sorted(list,key = lambda i:get_time(i))
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

def is_file(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            return True
        else:
            return False
    elif path.split('.')[-1] == 'html':
        return True
    else:
        return False

def is_dir(path):
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

def is_ignore(path):
    if is_dir(path):
        for i in get_config('Ignore'):
            if get_name(path).lower() == i.lower():
                return True
    else:
        return None

def initial():
    shutil.rmtree(get_config('Directory','Output'))
    os.mkdir(get_config('Directory','Output'))
    post_path = in_to_out(get_config('Directory','Post'))
    os.mkdir(post_path)
    asset_path = get_config('Directory','Asset')
    shutil.copytree(get_config('Directory','Asset'),get_config('Directory','Output')+'asset/')
    page_list = get_list('page')
    for page in page_list:
        page = in_to_out(page)
        page = remove_index(page)
        os.mkdir(page)
        #print(page)
