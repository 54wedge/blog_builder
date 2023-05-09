import sys

def sstyle(string, *args):
    style_dict = {'reset':'\033[00m', 'bold':'\033[01m', 'disable':'\033[02m',
        'underline':'\033[04m', 'reverse':'\033[07m', 'strikethrough':'\033[09m',
        'invisible':'\033[08m', 'black':'\033[30m', 'red':'\033[31m',
        'green':'\033[32m', 'orange':'\033[33m', 'blue':'\033[34m',
        'purple':'\033[35m', 'cyan':'\033[36m', 'lightgrey':'\033[37m',
        'darkgrey':'\033[90m', 'lightred':'\033[91m', 'lightgreen':'\033[92m',
        'yellow':'\033[93m', 'lightblue':'\033[94m', 'pink':'\033[95m',
        'lightcyan':'\033[96m'}
    for arg in args:
        string = style_dict[arg] + string
    return string + style_dict['reset']

def nsprint(string, color="white", styles=["none"], end = "\n", ignore = False):
    style_dict = {"none":"",'reset':'\033[00m', 'bold':'\033[01m', 'disable':'\033[02m',
        'underline':'\033[04m', 'reverse':'\033[07m', 'strikethrough':'\033[09m',
        'invisible':'\033[08m'}
    color_dict = {"white":"",'black':'\033[30m', 'red':'\033[31m',
        'green':'\033[32m', 'orange':'\033[33m', 'blue':'\033[34m',
        'purple':'\033[35m', 'cyan':'\033[36m', 'lightgrey':'\033[37m',
        'darkgrey':'\033[90m', 'lightred':'\033[91m', 'lightgreen':'\033[92m',
        'yellow':'\033[93m', 'lightblue':'\033[94m', 'pink':'\033[95m',
        'lightcyan':'\033[96m'}
    for style in styles:
        string = style_dict[style] + string
    string = color_dict[color] + string
    string = string + style_dict["reset"]
    if "-s" not in sys.argv or ignore != False:      # -s stands for silence
        print(string, end = end)