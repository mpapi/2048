#!/usr/bin/env python

"""
Given a dictionary of legal words on standard in, write a file to
stdout suitable to become a dict.js.
"""
from itertools import tee, izip_longest
import re
import sys

from jinja2 import Template

# We don't want proper nouns (capped) or anything with non-a-z except
# compound words, which we'll split.
NON_LEGAL_RE = re.compile(r'[^a-z -]')


def words(fh):
    for line in fh:
        line = line.strip()
        if NON_LEGAL_RE.search(line):
            continue
        space_delimited = line.split()
        for spaced in space_delimited:
            dash_delimeted = spaced.split('-')
            for dashed in dash_delimeted:
                yield dashed.lower()


def main(fh):
    with open('dict.js.jinja2', 'rb') as tfh:
        template = Template(tfh.read())

    legal_fragments = set()
    legal_words = set(words(fh))

    for word in legal_words:
        for start in range(len(word)):
            for end in range(start, len(word)):
                fragment = word[start:end]
                if fragment and fragment not in legal_words:
                    legal_fragments.add(fragment)

    print template.render(words=legal_words,
                          fragments=(legal_fragments - legal_words))


if __name__ == '__main__':
    main(sys.stdin)
