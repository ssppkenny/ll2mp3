import pathlib
from collections import namedtuple
import re

HEADER_REGEX = r'(PERFORMER) \"?([^\"]*)\"?.*|(TITLE) \"?([^\"]*)\"?.*'
TRACK_REGEX_TITLE = r'.*?(TRACK\s+(\d+).*?TITLE\s+\"?([^\"+]+)\"?.*?)'
TRACK_REGEX_PERFORMER = r'.*?(TRACK\s+(\d+).*?PERFORMER\s+\"?([^\"+]+)\"?.*?)'

CueSheet = namedtuple('CueSheet', ['performer', 'title', 'file', 'tracks'])
Track = namedtuple('Track', ['title', 'number'])


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
    tracks = [Track(x[2], x[1]) for x in re.findall(TRACK_REGEX_TITLE, t, re.DOTALL)]
    d['tracks'] = tracks
    #tracks = re.findall(TRACK_REGEX_PERFORMER, t, re.DOTALL)
    cuesheet = CueSheet(**d)
    return cuesheet


def find_cue_file(dir_name):
    for cuefile in pathlib.Path(dir_name).glob('*.cue'):
        return cuefile
    return None


