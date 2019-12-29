from bs4 import BeautifulSoup as bs
import tool.io as io
import tool.builder as builder

import yaml    #maybe

def load_template(name,option = None):
    path_header = builder.get_config('Directory','Template') + 'header.html'
    path_footer = builder.get_config('Directory','Template') + 'footer.html'
    path = builder.get_config('Directory','Template') + name
    template = io.html_open(path_header) + io.html_open(path) + io.html_open(path_footer)
    if option is None:
        return template
    elif option == 'soup':
        template_soup = bs(template,'html.parser')
        return template_soup

def get_meta(html):
    if type(html) is bs:
        html = str(html)
    html = html.split('<body>')[1]
    html = html.split('<hr')[0]      #for <hr /> <hr/> and <hr>
    #html = html.split('<hr/>')[0]   #not sure if it will always work
    #print(html)
    soup = bs(html,'html.parser')
    raw_meta = soup.get_text()
    try:
        meta = yaml.safe_load(raw_meta)
        #print(type(meta))
        #print(meta['Title'])
        if type(meta) is dict:
            return meta
        else:               #may be str type if raw_meta is not in yaml format
            return {}       #return empty dict
    except yaml.scanner.ScannerError:     ##may not needed
        return {}
        #print(html)

#def get_abstract(html):

def insert_nav(soup,option = None):
    if type(soup) is str:
        soup = bs(soup,'html.parser')
    new_a = a_href('Index','../index.html')
    new_nav = soup.new_tag('nav',id = 'nav-menu' )
    soup.container2.append(new_nav)
    soup.container2.nav.append(new_a)
    page_list = builder.get_list('page')
    for i in page_list:
        name = builder.get_name(i)
        path = '../' + name + '/index.html'
        new_a = a_href(name,path)
        soup.container2.nav.append(new_a)
    if option is None:
        template = str(soup)
        #io.save(template,'test','./test.index')
        return template
    elif option == 'soup':
        return soup

def insert_body(html,template,option = None):   ##need to exclude meta data
    if type(html) is bs:
        html = str(html)
    if type(template) is bs:
        template = str(template)
    html = html.split('<body>')[1]
    body = html.split('</body>')[0]
    html = template.replace('%%Body%%',body)
    if option is None:
        return html
    if option == 'soup':
        html = bs(html,'html.parser')
        return html

def insert_author(html,option = None):
    if type(html) is bs:
        html = str(html)
    html = html.replace('%%Author%%',builder.get_config('Meta','Author'))
    if option is None:
        return html
    if option == 'soup':
        html = bs(html,'html.parser')
        return html

'''
overridable author
'''

def insert_meta(html,meta,option = None):
    if type(html) is bs:
        html = str(html)
    for key in meta:
        html = html.replace('%%'+key+'%%', meta[key])
    if option is None:
        return html
    if option == 'soup':
        html = bs(html,'html.parser')
        return html

'''
~~what if the meta dict is empty~~
what if can't find place-holder
remove <h1>
tag list
category ignore
clickable
'''

def a_href(name,path):
    soup = bs('','html.parser')
    new_a = soup.new_tag('a',href = path)
    new_a.string = name
    return new_a
