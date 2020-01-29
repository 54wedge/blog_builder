import tool.utils as utils
from tool.builder import _Builder
from performance import method
import timeit

utils.initial()
builder = _Builder()    #for the sake of speed

t = method()
start = timeit.default_timer()
t+builder.build_page
t+builder.build_post
t+builder.build_index
t+builder.build_archive
t+builder.build_category
t+builder.build_category
t+builder.build_tag
stop = timeit.default_timer()
print('took Time: ' +str(stop - start))
