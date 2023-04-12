import tool.utils as utils
from tool.builder import _Builder
import os

root = os.path.abspath(__file__+"/../")
print(root)
os.chdir(root)
print('Initialing destination folder......')
# utils.initial()
print('Reading html file from source folder......')
builder = _Builder(root)    #for the sake of speed

builder.build_page()
builder.build_post()
builder.build_router()
