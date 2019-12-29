import tool.builder as builder
import tool.io as io
import tool.modifier as modifier

builder.initial()

#build page
for page_path in builder.get_list('page'):
    template = modifier.load_template('page.html')
    template = modifier.insert_nav(template)
    if builder.is_ignore(page_path):
        pass
    else:
        name = builder.get_name(page_path,'html')
        page_path = page_path + '/index.html'
        html = io.html_open(page_path)
        meta = modifier.get_meta(html)
        #print(meta)
        #print(type(meta))
        path = builder.in_to_out(page_path)
        path = builder.remove_index(path)
        page = modifier.insert_body(html,template)
        page = modifier.insert_author(page)
        page = modifier.insert_meta(page,meta)
        io.save(page,name,path,'prettify')

#build post
for post_path in builder.get_list('post'):
    template = modifier.load_template('post.html')
    template = modifier.insert_nav(template)
    name = builder.get_name(post_path,'html')
    path = builder.get_config('Directory','Post')
    path = builder.in_to_out(path)
    path = path + '/' + name + '.html'
    html = io.html_open(post_path)
    meta = modifier.get_meta(html)
    post = modifier.insert_body(html,template)
    post = modifier.insert_author(post)
    post = modifier.insert_meta(post,meta)
    io.save(post,name,path,'prettify')

#build index

#build archive

#build tag

#build category
