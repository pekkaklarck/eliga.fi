#!/usr/bin/env python3.6

from pathlib import Path
import re
from shutil import copy

from docutils.core import publish_parts
from docutils.writers.html5_polyglot import Writer as HtmlWriter

template = Path('src/TEMPLATE.html').read_text()

for path in Path('src').glob('*.rst'):
    content = publish_parts(path.read_text(), writer=HtmlWriter())['html_body']
    content = re.sub(r'href="(.*)\.rst"', r'href="\1"', content)
    with open(f'docs/{path.stem}.html', 'w') as f:
        print(f'Generate {f.name}')
        f.write(template.replace('[CONTENT HERE]', content))

for extension in ['css', 'png']:
    for path in Path('src').glob(f'*.{extension}'):
        print(f'Copy {path} -> docs/{path.name}')
        copy(path, f'docs/{path.name}')
