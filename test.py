import ll2mp3
import pathlib

if __name__ == '__main__':
    p = pathlib.Path('/Users/ugxnbmikhs/code/python/ll2mp3')
    fp = p.resolve()
    cuepath = ll2mp3.find_cue_file(fp)
    cue_file = ll2mp3.parse_cue_file(cuepath)
    audio_file = cue_file.file
    ll2mp3.convert(cuepath.resolve(), cue_file)



