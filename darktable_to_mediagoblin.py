#!/usr/bin/env python
"""
Generate a mediagoblin batch upload package based off the metadata
from darktable-generated XML files.

Copyright 2017 George C. Privon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import re
import sys
import glob
import argparse
from lxml import etree


def get_args():
    """
    Parse arguments
    """

    parser = argparse.ArgumentParser(description="Generate mediagoblin batch \
upload files from darktable metadata.")
    parser.add_argument('--outfile', '-o', type='str', default='upload.csv',
                        help='Output csv file for batch upload.')
    parser.add_argument('searchdir', type='str', default='./',
                        help='Directory to search for darktable_exported \
files.')

    return parser.parse_args()


def find_folders(path):
    """
    Given a directory, return a list of sub-folders containing
    'darktable_exported' folders.
    """

    return folders


def get_tags(fname):
    """
    Read a specified darktable xml file and return the title and tags.
    """

    errreturn = ''

    if not os.path.isfile(fname):
        return errreturn

    mdata = etree.parse(fname)

    xmlroot = mdata.getroot()

    if not re.search('xmpmeta', xmlroot.tag):
        return errreturn

    for elem in xmlroot.getchildren():
        if re.search('RDF', elem.tag):
            continue

    for selem in elem.getchildren():
        if re.search('Description', selem.tag):
            continue

    for sselem in selem.getchildren():
        if re.search('subject', sselem.tag):
            continue

    tags = []

    for tag in sselem.getchildren()[0].getchildren():
        tags.append(tag.text)

    return tags


def main():
    """
    do the main things
    """

    args = get_args()

    outf = open(args.outfile, 'w')

    outf.write('"location","title","tags"\n')

    folders = find_folders(args.searchdir)

    for folder in folders:
        files = glob.glob(folder + 'darktable_exported/*.jpg')

        for fname in files:
            if not os.path.isfile(fname):
                sys.stderr.write(fname + ' not found. Skipping.\n')
            outf.write(fname + ',"')
            iname = fname.split('darktable_exported/')[-1].split('.jpg')[0]
            tags = get_tags(folder + iname + '.xmp')
            if title == 'nofile':
                title = iname
            outf.write('"' + title + '","')
            outf.write(tags + '"\n')

    outf.close()

if __name__ == "__main__":
    main()
