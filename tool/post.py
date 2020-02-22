import tool.utils as utils
from tool.page import _Page


class _Post(_Page):
    def __init__(self,path,prev_post=None,next_post=None):
        _Page.__init__(self,path)
        self.path_out = utils.in_to_out(self.path)
        self.type = 'post'
        if prev_post is None:
            self.prev_post_link = ''
        else:
            self.prev_post_link = str(prev_post.link)
        if next_post is None:
            self.next_post_link = ''
        else:
            self.next_post_link = str(next_post.link)

    def build(self):
        _Page.build(self)
        #self.content = self.content.replace('%%Prev-post%%',self.prev_post_link)
        #self.content = self.content.replace('%%Next-post%%',self.next_post_link)
