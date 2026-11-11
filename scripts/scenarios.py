#!/usr/bin/env python3
import json, re
from pathlib import Path
import yaml
s = (Path(__file__).resolve().parent.parent / 'template.tpl').read_text()
p = re.split(r'(?m)^___([^\n]+)___\s*$', s)
d = dict(zip(p[1::2], p[2::2]))
print(json.dumps({'js':d['SANDBOXED_JS_FOR_WEB_TEMPLATE'], 'tests':yaml.safe_load(d['TESTS'])}))
