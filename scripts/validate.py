#!/usr/bin/env python3
import base64, json, re, subprocess, tempfile
from pathlib import Path
import yaml

root = Path(__file__).resolve().parent.parent
text = (root / 'template.tpl').read_text(encoding='utf-8-sig')
pieces = re.split(r'(?m)^___([^\n]+)___\s*$', text)
sections = dict(zip(pieces[1::2], pieces[2::2]))
assert set(sections) == {'INFO', 'TEMPLATE_PARAMETERS', 'SANDBOXED_JS_FOR_WEB_TEMPLATE', 'WEB_PERMISSIONS', 'TESTS', 'TERMS_OF_SERVICE', 'NOTES'}
info = json.loads(sections['INFO']); params = json.loads(sections['TEMPLATE_PARAMETERS']); permissions = json.loads(sections['WEB_PERMISSIONS']); tests = yaml.safe_load(sections['TESTS'])
assert info['categories'] == ['PERSONALIZATION', 'ANALYTICS']
assert len(tests['scenarios']) == 5 and tests['setup']
platform = next(p for p in params if p['name'] == 'platform')
assert [x['value'] for x in platform['selectItems']] == ['vtex','vtexio','shopify','nuvemshop','magento1x','magento2x','wordpress']
assert next(p for p in params if p['name']=='env')['defaultValue'] == 'production'
for name in ('accountId','cookieDomain','platform'):
 assert any(v['type']=='NON_EMPTY' for v in next(p for p in params if p['name']==name)['valueValidators'])
image = base64.b64decode(info['brand']['thumbnail'].split(',',1)[1], validate=True)
assert len(image) < 50000
with tempfile.NamedTemporaryFile(suffix='.png') as f:
 f.write(image); f.flush(); assert subprocess.check_output(['magick','identify','-format','%m %wx%h',f.name],text=True) == 'PNG 96x96'
by_id = {p['instance']['key']['publicId']: p for p in permissions}
assert set(by_id) == {'access_globals','inject_script','logging'}
def values(pid): return by_id[pid]['instance']['param'][0]['value']
assert values('logging')['string'] == 'debug'
assert {v['string'] for v in values('inject_script')['listItem']} == {'https://c.usebeon.io/v6/loader.js','https://c.staging.usebeon.io/v6/loader.js'}
actual = {}
for item in values('access_globals')['listItem']:
 fields = {k['string']: v.get('string',v.get('boolean')) for k,v in zip(item['mapKey'],item['mapValue'])}; actual[fields['key']] = (fields['read'],fields['write'],fields['execute'])
expected = {k:(True,True,False) for k in ('beonobject','beon','beon.q','beon.l','beonConfig')}
expected.update({k:(True,False,False) for k in ('beonly._coreVersion','beonly.account','beonly.platform','beonly.env','beonly.cookiedomain','beonly.inited','beone.inited')})
assert actual == expected
js = sections['SANDBOXED_JS_FOR_WEB_TEMPLATE']
for api,mode in [('copyFromWindow',0),('setInWindow',1)]:
 for key in re.findall(r"\b"+api+r"\('([^']+)'",js): assert actual[key][mode], (api,key)
assert "createArgumentsQueue('beon', 'beon.q')" in js and all(actual[k][:2] == (True,True) for k in ('beon','beon.q'))
assert all((root / f).is_file() for f in ('template.tpl','metadata.yaml','LICENSE','README.md'))
assert len(list(root.rglob('template.tpl'))) == 1
assert 'Apache License' in (root/'LICENSE').read_text() and 'Version 2.0, January 2004' in (root/'LICENSE').read_text()
metadata = yaml.safe_load((root/'metadata.yaml').read_text()); assert metadata['homepage'] == 'https://www.beonly.com.br' and metadata['documentation'] == 'https://github.com/beonica/bn.core.tags.studiov6#readme'
sha = metadata['versions'][0]['sha']; assert re.fullmatch(r'[0-9a-f]{40}',sha)
assert subprocess.check_output(['git','show',f'{sha}:template.tpl'],cwd=root) == (root/'template.tpl').read_bytes()
print('Estrutura, JSON/YAML, plataforma, ícone, permissões e SHA: OK')
