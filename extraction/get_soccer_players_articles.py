#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
given the corpus directory, in which there is one file per article,
extracts al the files containing an article whose wikipedia id
is contained in the input list (one id per like)
"""

import os
import re
import shutil
import sys


DEBUG = True


def load_wiki_ids(filein):
    with open(filein) as i:
        return {l.strip() for l in i}


def extract_soccer_articles(soccer_ids, corpus_dir, output_dir):
    for path, subdirs, files in os.walk(corpus_dir):
        for name in files:
            f = os.path.join(path, name)
            with open(f) as i:
                content = i.read()

            match = re.search('id="([^"]+)"', content)
            if not match:
                continue

            current_id = match.group(1)
            if DEBUG:
                print "File = [%s] - Wiki ID = [%s]" % (f, current_id)
            if current_id in soccer_ids:
                shutil.copy(f, output_dir)
                if DEBUG:
                    print "MATCHED! [%s]" % content
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: %s <SOCCER_IDS> <CORPUS_DIR> <OUTPUT_DIR>" % __file__
        sys.exit(1)
    else:
        ids = load_wiki_ids(sys.argv[1])
        extract_soccer_articles(ids, sys.argv[2], sys.argv[3])
