"""Збирає сайт: кожен файл з src/ -> <slug>/index.html, плюс головна сторінка зі списком.
Запуск: python3 build.py  (src/ — копія папки «Сайти-тести»)"""
import json, os, shutil, html
ROOT = os.path.dirname(os.path.abspath(__file__))
sites = json.load(open(os.path.join(ROOT, 'sites.json'), encoding='utf-8'))
for s in sites:
    d = os.path.join(ROOT, s['slug']); os.makedirs(d, exist_ok=True)
    shutil.copyfile(os.path.join(ROOT, 'src', s['file']), os.path.join(d, 'index.html'))
order = ['Алгебра', 'Хімія', 'Фронтенд']
def gk(g):
    try: return float(g.split('–')[0])
    except: return 99
groups = ''
for subj in order:
    items = sorted([s for s in sites if s['subject'] == subj], key=lambda s: (gk(s['grade']), s['title']))
    if not items: continue
    rows = ''.join(f'''
      <li><a href="{s['slug']}/"><span class="g">{html.escape(s['grade'] + ' клас') if s['grade'] else '—'}</span><span class="t">{html.escape(s['title'])}</span><span class="go" aria-hidden="true">→</span></a></li>''' for s in items)
    groups += f'''
    <section class="grp"><h2>{subj}</h2><ul>{rows}
    </ul></section>'''
tpl = open(os.path.join(ROOT, 'index.template.html'), encoding='utf-8').read()
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(tpl.replace('<!--GROUPS-->', groups))
print('built', len(sites), 'sites')
