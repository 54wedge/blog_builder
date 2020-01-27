import cProfile
import pstats
from pstats import SortKey
import timeit

CRED = '\033[91m'
CEND = '\033[0m'

class method():
    def __add__(self, other):
        t_test(other)
    def __sub__(self,other):
        p_test(other)
    def __mul__(self,other):
        t_test(other)
        p_test(other)

def t_test(func):
    start = timeit.default_timer()
    func()
    stop = timeit.default_timer()
    print(CRED + func.__name__ + '() took Time: ' +str(stop - start) + CEND)

def p_test(func):
    profile = cProfile.Profile()
    profile.runcall(func)
    with open('./performance/'+func.__name__+'.txt','w') as txt:
        ps = pstats.Stats(profile,stream = txt).sort_stats(SortKey.CUMULATIVE)
        ps.print_stats(20)
    print(CRED + func.__name__ + '() performance file generated at ' +'./performance/'+func.__name__+'.txt' + CEND)
    #ps.print_stats()
