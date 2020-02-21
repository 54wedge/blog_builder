import tool.utils as utils
from tool.builder import _Builder

print('Initialing destination folder......')
utils.initial()
print('Reading html file from source folder......')
builder = _Builder()    #for the sake of speed

print('Building pages......')
builder.build_page()
print('Building posts......')
builder.build_post()
print('Building Home page......')
builder.build_home()
print('Building Archive page......')
builder.build_archive()
print('Building Category pages......')
builder.build_category()
print('Building Tag pages......')
builder.build_tag()
