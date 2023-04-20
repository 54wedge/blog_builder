import os
import sys
import yaml
import tool.utils as utils

class _Config:
    def __init__(self, path):
        self.config_path = path
        with open(path, 'r') as config:
            tmp = yaml.safe_load(config)
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

if "-c" in sys.argv:
    config_path = sys.argv[sys.argv.index("-c")+1]
else:
    config_path = os.path.join(os.getcwd(),sys.argv[0])
    config_path = os.path.abspath(config_path+"/../")
    config_path = os.path.join(config_path,"./config.yml")
    config_path = os.path.abspath(config_path)
utils.nsprint("Looking for config file at " + config_path)
config = _Config(config_path)