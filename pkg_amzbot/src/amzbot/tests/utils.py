import os, json
from pathlib import Path


def get_testlist(classname):
    # opening testlist.json file
    content = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testlists', '{}_testlist.json'.format(classname))).read_text()
    data = json.loads(content)
    return [] if 'tests' not in data else data['tests']
