"""Host-side tool: splits ActOne/ActTwo/Dialogs into one module per level and compiles them.

Level lambdas keep their whole module alive, so loading only the current level's
code keeps RAM free on the Thumby. Each Lvl<N>.mpy holds that level plus its intro dialogs.
Also compiles the core modules to .mpy (delete their .py copies on the device so the .mpy is imported).

Usage: python3 build_levels.py   (mpy-cross must be on PATH)
"""
import re
import subprocess

WORDS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']


def split_blocks(text, pattern):
    matches = list(re.finditer(pattern, text, re.M))
    head = text[:matches[0].start()]
    blocks = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((m.group(1), text[m.start():end].rstrip() + '\n'))
    return head, blocks


def compile_module(name, source):
    with open(name + '.py', 'w') as f:
        f.write(source)
    subprocess.check_call(['mpy-cross', '-O3', '-X', 'no-source-lines', name + '.py'])
    import os
    os.remove(name + '.py')


def dialog_blocks():
    text = open('Dialogs.py').read()
    body = text[text.index('class LevelDialogs'):]
    zip_helper = re.search(r'^    def _zip_dialogs.*?(?=^    def )', body, re.M | re.S).group(0)
    _, blocks = split_blocks(body, r'^    def _build_level_(\w+)_dialogs\(')
    result = {}
    for word, block in blocks:
        block = block.split('\n    def get_dialogs_for_level')[0].rstrip() + '\n'
        block = block.replace('def _build_level_%s_dialogs' % word, 'def build', 1)
        helper = zip_helper if '_zip_dialogs' in block else ''
        result[WORDS.index(word) + 1] = 'class LevelDialogs:\n' + helper + block
    return result


def build_levels(src, cls, dialogs):
    text = open(src).read()
    class_start = text.index('class ' + cls)
    head = text[:class_start]
    _, blocks = split_blocks(text[class_start:], r'^\tdef _build_level(\d+)\(')
    for number, block in blocks:
        compile_module('Lvl' + number, head + 'class %s:\n' % cls + block + '\n' + dialogs[int(number)])

dialogs = dialog_blocks()
build_levels('Levels.py', 'ActOneLevels', dialogs)

CORE = ['Shared', 'GameState', 'Menus', 'Items', 'MapData', 'Callbacks']
for name in CORE:
    subprocess.check_call(['mpy-cross', '-O3', '-X', 'no-source-lines', name + '.py'])

