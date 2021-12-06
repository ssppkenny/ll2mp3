import ll2mp3
import pathlib

if __name__ == '__main__':
    p = pathlib.Path('/Users/ugxnbmikhs/code/python/ll2mp3')
    fp = p.resolve()
    print(fp)
    cuepath = ll2mp3.find_cue_file(fp)
    ll2mp3.parse_cue_file(cuepath)





