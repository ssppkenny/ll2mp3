import pathlib
from collections import namedtuple
import re
import os
import eyed3

HEADER_REGEX = r'(PERFORMER) \"?([^\"]*)\"?.*|(TITLE) \"?([^\"]*)\"?.*'
TRACK_REGEX_TITLE = r'.*?(TRACK\s+(\d+).*?TITLE\s+\"?([^\"+]+)\"?.*?)'
TRACK_REGEX_PERFORMER = r'.*?(TRACK\s+(\d+).*?PERFORMER\s+\"?([^\"+]+)\"?.*?)'

CueSheet = namedtuple('CueSheet', ['performer', 'title', 'file', 'tracks'])
Track = namedtuple('Track', ['title', 'number'])


def parse_cue_file(path):
    d = {}
    with open(path.resolve(), "r") as f:
        text = f.read()
    file = re.findall(r'FILE \"?([^\"]*)\"? .*\n', text)
    file, *_ = file
    d['file'] = pathlib.Path(path.parent, file)
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

def convert(cue_file, cuesheet):
    audio_file = cuesheet.file.resolve()
    cmd = f'cuebreakpoints "{cue_file}" | sed s/$/0/ | shnsplit -O always -o flac "{audio_file}"'
    ret_code = os.system(cmd)
    if ret_code != 0:
        convert_to_wav_and_back(audio_file)
        cmd = f'cuebreakpoints "{cue_file}" | sed s/$/0/ | shnsplit -O always -o flac "{audio_file}.flac"'
        os.system(cmd)

    convert_files(cuesheet)
    delete_old_files(cuesheet)

def delete_old_files(cuesheet):
    pd = cuesheet.file.parent.resolve()
    cmd = f'rm -rf {pd}/*.flac'
    os.system(cmd)
    cmd = f'rm -rf {pd}/*.wav'
    os.system(cmd)


def convert_to_wav_and_back(audio_file):
    cmd = f'ffmpeg -y -i "{audio_file}" "{audio_file}.wav"'
    os.system(cmd)
    cmd = f'ffmpeg -y -i "{audio_file}.wav" "{audio_file}.flac"'
    os.system(cmd)

def convert_files(cuesheet):
    pd = cuesheet.file.parent.resolve()
    for track in cuesheet.tracks:
        src = f"split-track{track.number}.flac"
        src = f"{pd}/{src}"
        dst = f"{pd}/{track.title}.mp3"
        cmd = f'ffmpeg -y -i "{src}" -ab 320k "{dst}"'
        os.system(cmd)
        mp3_file = eyed3.load(dst)
        mp3_file.initTag()
        mp3_file.tag.artist = cuesheet.performer
        mp3_file.tag.title = track.title
        mp3_file.tag.save(dst)








