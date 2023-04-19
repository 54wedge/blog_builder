import tool.utils as utils
from tool.builder import _Builder
import os

root = os.path.abspath(__file__+"/../")
if os.getcwd() != root:
    print("Relocating to " + root)
    os.chdir(root)

builder = _Builder(root)    #for the sake of speed

builder.build_page()
builder.build_post()
builder.build_router()
