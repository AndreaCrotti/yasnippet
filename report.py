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
        assert self.name is not None, "%s\n %s" % ('name', snippet)
        self.key = extract_variable(snippet, 'key')
        self.group = extract_variable(snippet, 'group')

    def __str__(self):
        return "{}: {}".format(self.name, self.key)


def main(directory):
    for root, dirs, files in walk(directory):
        for fi in files:
            full_path = path.join(root, fi)
            with open(full_path) as opened:
                if fi.startswith('.'):
                    continue

                text = opened.read()
                print(Snippet(text))


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
