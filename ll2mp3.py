import pathlib
from collections import namedtuple
import re

HEADER_REGEX = r'(PERFORMER) \"?([^\"]*)\"?.*|(TITLE) \"?([^\"]*)\"?.*'
TRACK_REGEX = r'(PERFORMER) \"?([^\"]*)\"?.*|(TITLE) \"?([^\"]*)\"?.*'

Header = namedtuple('Header', ['performer', 'title', 'file', 'tracks'])
Track =namedtuple('Track', ['performer', 'title'])


def parse_cue_file(path):
    d = {}
    with open(path.resolve(), "r") as f:
        text = f.read()
    file = re.findall(r'FILE \"?(.*)\"? .*\n', text)
    file, *_ = file
    d['file'] = file
    h, t = re.split(r"FILE.*\n", text, re.DOTALL)
    for line in h.split('\n'):
        l = re.findall(HEADER_REGEX, line)
        if l:
            words, *_ = l
            words = [w for w in words if w]
            if words:
                attr, val, *_ = words
                attr = attr.lower()
                d[attr] = val




def find_cue_file(dir_name):
    for cuefile in pathlib.Path(dir_name).glob('*.cue'):
        return cuefile
    return None


