import htmlmin
from bs4 import BeautifulSoup as bs

def html_open(path,option = None):
    with open(path,'r') as html:
        html = html.read()
    if option is None:
        return html
    elif option == 'minify':
        mini_html = htmlmin.minify(html)
        return mini_html
    elif option == 'soup':
        soup = bs(html,'html.parser')
        return soup

def save(html,name,path,option = None):
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
        soup = bs(html,'html.parser')
        with open(path,'w') as output:
            output.write(soup.prettify())
