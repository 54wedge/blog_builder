import os
import htmlmin
from bs4 import BeautifulSoup as bs
import sys

def sstyle(string, *args):
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

def nsprint(string, color="white", styles=["none"], end = "\n", ignore = False):
    style_dict = {"none":"",'reset':'\033[00m', 'bold':'\033[01m', 'disable':'\033[02m',
        'underline':'\033[04m', 'reverse':'\033[07m', 'strikethrough':'\033[09m',
        'invisible':'\033[08m'}
    color_dict = {"white":"",'black':'\033[30m', 'red':'\033[31m',
        'green':'\033[32m', 'orange':'\033[33m', 'blue':'\033[34m',
        'purple':'\033[35m', 'cyan':'\033[36m', 'lightgrey':'\033[37m',
        'darkgrey':'\033[90m', 'lightred':'\033[91m', 'lightgreen':'\033[92m',
        'yellow':'\033[93m', 'lightblue':'\033[94m', 'pink':'\033[95m',
        'lightcyan':'\033[96m'}
    for style in styles:
        string = style_dict[style] + string
    string = color_dict[color] + string
    string = string + style_dict["reset"]
    if "-s" not in sys.argv or ignore != False:      # -s stands for silence
        print(string, end = end)

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

def html_open(path,option = None):
    with open(path,'r') as html:
        html = html.read()
    if option is None:
        return html
    elif option == 'soup':
        soup = bs(html,'lxml')
        return soup

def safe_save(html,path,option = 'str'):
    dir_path = path.rsplit('/',1)[0]
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
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

def str_to_bs(html):
    soup = bs(html,'lxml')
    return soup

empty_soup = bs('','lxml')

def a_href(name,path):
    new_a = empty_soup.new_tag('a',href = path)
    new_a.string = name
    return new_a
