import tool.builder as builder
import tool.io as io

from tool.modifier import _Page
from tool.modifier import _Post
from tool.modifier import _Template
from tool.modifier import _Archive

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
archive = _Archive()
io.save(archive.print(),'./dist/Archive/index.html','prettify')
#build tag

#build category
