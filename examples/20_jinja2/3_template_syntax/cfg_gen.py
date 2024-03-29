# -*- coding: utf-8 -*-
import os
import sys

import yaml
from jinja2 import Environment, FileSystemLoader

#$ python cfg_gen.py templates/for.txt data_files/for.yml
template_dir, template_file = os.path.split(sys.argv[1])

vars_file = sys.argv[2]

env = Environment(
    loader=FileSystemLoader(template_dir),
    trim_blocks=False,
    lstrip_blocks=False)
template = env.get_template(template_file)

with open(vars_file) as f:
    vars_dict = yaml.safe_load(f)

print(template.render(vars_dict))
