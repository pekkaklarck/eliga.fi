#!/usr/bin/env python3.6

from pathlib import Path
import re
from shutil import copy

from docutils.core import publish_parts
from docutils.writers.html5_polyglot import Writer as HtmlWriter

TEMPLATE = Path('src/TEMPLATE.html').read_text()
RESOURCES = ['css', 'png', 'jpg']


def build_directory(directory, level=0):
    for path in directory.iterdir():
        if path.is_dir():
            build_directory(path, level+1)
        elif path.suffix == '.rst':
            build_file(path, level)
        elif path.suffix[1:] in RESOURCES:
            copy_file(path)


def build_file(path, level):
    content = publish_parts(
        path.read_text(),
        writer=HtmlWriter(),
        settings_overrides={'doctitle_xform': False}
    )['html_body']
    content = re.sub(r'href="(.*)\.rst"', r'href="\1.html"', content)
    template = get_template(level)
    output = Path('docs', *path.parts[1:]).with_suffix('.html')
    print(f'Generate {output}')
    output.write_text(template.replace('[CONTENT HERE]', content))


def get_template(level):
    prefix = '../' * level
    template = re.sub(r'href="(.*)\.css"', fr'href="{prefix}\1.css"', TEMPLATE)
    template = re.sub(r'href="\./', fr'href="{prefix}', template)
    return template


def copy_file(path):
    print(f'Copy {path} -> docs/{path.name}')
    copy(path, f'docs/{path.name}')


build_directory(Path('src'))
