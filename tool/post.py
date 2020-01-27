import tool.utils as utils

from tool.page import _Page

class _Post(_Page):
    def __init__(self,path):
        _Page.__init__(self,path)
        self.path_out = utils.in_to_out(self.path)
        self.type = 'post'
