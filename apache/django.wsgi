import os
import sys

paths = [ '/Users/hobbes3/Sites/mysite',
          '/usr/local/Cellar/python/2.7.2/lib/python2.7/site-packages',
]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

sys.executable = '/usr/local/bin/python'
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
