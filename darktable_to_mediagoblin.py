#!/usr/bin/env python
"""
Generate a mediagoblin batch upload package based off the metadata
from darktable-generated XML files.

Version 0.1.1

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
    parser.add_argument('--outfile', '-o', type=str, default='upload.csv',
                        help='Output csv file for batch upload.')
    parser.add_argument('searchdir', type=str, default='./',
                        help='Directory to search for darktable_exported \
files.')

    return parser.parse_args()


def find_folders(path):
    """
    Given a directory, return a list of sub-folders containing
    'darktable_exported' folders.
    """

    folders = []

    subdirs = os.walk(path)
    for directory in subdirs:
        if re.search('darktable_exported', directory[0]):
            folders.append(directory[0])

    return folders


def get_metadata(fname):
    """
    Read a specified darktable xml file and return the title and tags.
    """

    metadata = {'title': '',
                'tags': [],
                'desc': ''}
    errreturn = metadata

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
        if re.search('title', sselem.tag):
            metadata['title'] = sselem.getchildren()[0].getchildren()[0].text
        elif re.search('description', sselem.tag):
            metadata['desc'] = sselem.getchildren()[0].getchildren()[0].text
        elif re.search('subject', sselem.tag):
            for tag in sselem.getchildren()[0].getchildren():
                metadata['tags'].append(tag.text)

    return metadata


def main():
    """
    do the main things
    """

    args = get_args()

    outf = open(args.outfile, 'w')

    outf.write('location,dc:title,dc:tags\n')

    folders = find_folders(args.searchdir)

    for folder in folders:
        files = sorted(glob.glob(folder + '/*.jpg'))

        for fname in files:
            if not os.path.isfile(fname):
                sys.stderr.write(fname + ' not found. Skipping.\n')
            outf.write('"' + fname + '",')
            iname = fname.split('darktable_exported/')[-1].split('.jpg')[0]
            if re.search('\d\d\d\d-\d\d-\d\d', iname):
                mname = iname.rsplit('-', maxsplit=1)[1]
            else:
                mname = iname
            mname = folder.split('darktable_exported')[0] + mname + '.CR2.xmp'
            mdata = get_metadata(mname)
            if mdata['title'] == '':
                mdata['title'] = iname
            outf.write('"' + mdata['title'] + '","')
            outf.write(','.join(mdata['tags']) + '"\n')

    outf.close()

if __name__ == "__main__":
    main()
