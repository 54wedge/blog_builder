import tool.builder as builder
import tool.io as io
import tool.modifier as modifier

from tool.modifier import _Page
from tool.modifier import _Post

builder.initial()

#build page
for page_path in builder.get_list('page'):
    if builder.is_page_ignore(page_path):
        pass
    else:
        page_path = builder.append_html(page_path)
        page = _Page(page_path)
        io.save(page.print(),page.name,page.path_out,'prettify')
#build post
for post_path in builder.get_list('post'):
    post = _Post(post_path)
    io.save(post.print(),post.name,post.path_out,'prettify')

#build index

#build archive

#build tag

#build category
