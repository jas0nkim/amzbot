import json
from pathlib import Path


def get_testlist(classname):
    # opening testlist.json file
    content = Path('htmls/{}_testlist.json'.format(classname)).read_text()
    data = json.loads(content)
    return [] if 'tests' not in data else data['tests']
