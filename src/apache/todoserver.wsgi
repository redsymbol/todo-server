#!/usr/bin/env python
import sys
import logging
import site

site.addsitedir('/srv/VENV/todoapi/lib/python3.4/site-packages')
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/srv/todoapi")

from todoserver import app as application
