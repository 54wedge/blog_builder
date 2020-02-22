import tool.utils as utils
from tool.builder import _Builder

print('Initialing destination folder......')
utils.initial()
print('Reading html file from source folder......')
builder = _Builder()    #for the sake of speed

builder.build_page()
builder.build_post()
builder.build_home()
builder.build_archive()
builder.build_category()
builder.build_tag()
