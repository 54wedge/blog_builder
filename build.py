import tool.builder as builder
import tool.io as io

from tool.modifier import _Page
from tool.modifier import _Post
from tool.modifier import _Template
from tool.modifier import _Archive
from tool.modifier import _Category
from tool.modifier import _Tag

builder.initial()

#build page
for page_path in builder.get_list('page'):
    if builder.is_page_ignore(page_path):
        pass
    else:
        page_path = builder.append_html(page_path)
        page = _Page(page_path)
        io.save(page.print(),page.path_out,'prettify')
#build post
for post_path in builder.get_list('post'):
    post = _Post(post_path)
    io.save(post.print(),post.path_out,'prettify')

#build index

#build archive
io.save(_Archive().print(),_Archive().path_out,'prettify')
#build tag

#build category
name_list = _Category().category_dict
for category_name, category_page in zip(name_list, _Category().print()):
    #print(category_page)
    path_out = builder.get_config('Directory','Output') + 'category/' + category_name + '/index.html'
    #print(path_out)
    builder.check_path(path_out)
    category_page = category_page.replace('../','../../')
    io.save(category_page,path_out,'prettify')

#build tag
name_list = _Tag().tag_dict
for tag_name, tag_page in zip(name_list, _Tag().print()):
    #print(tag_page)
    path_out = builder.get_config('Directory','Output') + 'tag/' + tag_name + '/index.html'
    #print(path_out)
    builder.check_path(path_out)
    tag_page = tag_page.replace('../','../../')
    io.save(tag_page,path_out,'prettify')
