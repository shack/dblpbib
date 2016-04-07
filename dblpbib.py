#! /usr/bin/env python3

import sys 
import re
import argparse
import urllib.request

dblp_key_pat = '(\w+/)*\w+'
bibtex_key_pat = """([A-Za-z0-9.:;?!`'()/*@_+=,]|-)+"""

def extract_bibtex_dblp_key(f):
    pat = re.compile('@\w+{DBLP:(' + dblp_key_pat + ')')
    for l in f:
        for m in pat.finditer(l):
            yield m.group(1)


def extract_dblp_cite(f):
    cite_pat = re.compile(r"\\[a-z]*cite[a-z]*{(" + bibtex_key_pat + ")}")
    dblp_pat = re.compile("DBLP:(" + dblp_key_pat + ")")
    for l in f:
        for m in cite_pat.finditer(l):
            keys = m.group(1)
            for k in dblp_pat.finditer(keys):
                yield k.group(1)

def download_dblp(key):
    url = 'http://dblp.uni-trier.de/rec/bib2/{}.bib'.format(key)
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    return text

parser = argparse.ArgumentParser(
        description="download bibtex entries found in .tex files from DBLP",
        epilog="""This tools scans the .tex files given as arguments for DBLP citekeys (e.g. \cite{DBLP:journals/iandc/Knuth65}).
               If the output bibliography (specified by -o) does not contain an appropriate bibtex entry, it 
               downloads that entry from DBLP and appends it to the output bibliography.

               Other than appending the downloaded entry, it will not modify the output bibliography in any way.""")
parser.add_argument('infiles', metavar="file", type=str, nargs='+', help='input tex files to scan for citations')
parser.add_argument("-o", "--output",  required=True, help="output bibliography to add missing entries to", type=str)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

keys_present = set()
keys_new     = set()

try:
    bib = open(args.output, 'r')
    for key in extract_bibtex_dblp_key(bib):
        if args.verbose:
            print('{} in bibfile'.format(key))
        keys_present.add(key)
except FileNotFoundError:
    pass

for fn in args.infiles:
    with open(fn, 'r') as f, open(args.output, 'a') as out:
        for key in extract_dblp_cite(f):
            have_to_download = not key in keys_present and not key in keys_new
            if args.verbose:
                print('{}: {}'.format(key, 'downloading' if have_to_download else 'available'))
            if have_to_download:
                entry = download_dblp(key)
                out.write(entry)
                keys_new.add(key)
