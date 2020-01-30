import tool.utils as utils
from tool.builder import _Builder

utils.initial()
builder = _Builder()    #for the sake of speed

builder.build_page()
builder.build_post()
builder.build_index()
builder.build_archive()
builder.build_category()
builder.build_category()
builder.build_tag()
