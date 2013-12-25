import argparse
import re

from collections import namedtuple
from os import walk, path


SAMPLE_SNIPPET = """
# -*- mode: snippet -*-
# name: project
# key: proj
# --
<project name="${1:test}" default="${2:compile}" basedir="${3:.}">"""

VAR_REGEXP_ST = r'#\s*{}\s*:\s*(.*)'


def extract_variable(snippet, variable):
    regexp = re.compile(VAR_REGEXP_ST.format(variable))
    found = regexp.search(snippet)
    if found is not None:
        return found.group(1)


class Snippet(object):
    def __init__(self, snippet):
        self.name = extract_variable(snippet, 'name')
        self.key = extract_variable(snippet, 'key')
        self.group = extract_variable(snippet, 'group')

    def __str__(self):
        return "{}: {}".format(self.name, self.key)


def main(directory):
    for root, dirs, files in walk(directory):
        for fi in files:
            with open(path.join(root, fi)) as opened:
                print(opened.read())
                print(Snippet(opened.read()))


def test_parsing():
    samp = Snippet(SAMPLE_SNIPPET)
    assert samp.name == 'project'
    assert samp.key == 'proj'
    assert samp.group is None


if __name__ == '__main__':
    # test_parsing()
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='snippets directory position')

    ns = parser.parse_args()
    main(ns.directory)
