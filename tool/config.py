from os import path, getcwd
from sys import argv as args
from yaml import safe_load as read_config
from tool.utils import nsprint

class _Config:
    def __init__(self, path):
        self.config_path = path
        with open(path, 'r') as config:
            tmp = read_config(config)
        self.input_path = tmp["Path"]["Input"]
        self.output_path = tmp["Path"]["Output"]
        self.template_path = tmp["Path"]["Template"]

        self.home_page_title = tmp["Site"]["Home_page_title"]
        self.site_prefix = tmp["Site"]["Prefix"]
        self.site_author = tmp["Site"]["Author"]
        self.home_size = tmp["Site"]["Home_size"]
        self.time_style = tmp["Site"]["Time_style"]
        self.archive_group = tmp["Site"]["Archive_group_by"]

        self.hide_meta = tmp["Content"]["Hide_meta"]
        self.save_style = tmp["Content"]["Save_style"]

        self.page_name_list = tmp["Page_list"]

if "-c" in args:
    config_path = args[args.index("-c")+1]
else:
    config_path = path.join(getcwd(),args[0])
    config_path = path.abspath(config_path+"/../")
    config_path = path.join(config_path,"./config.yml")
    config_path = path.abspath(config_path)
nsprint("Looking for config file at " + config_path)
config = _Config(config_path)