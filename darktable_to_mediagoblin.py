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
import sys
import glob
import argparse


def getArgs():
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


def findFolders(path):
    """
    Given a directory, return a list of sub-folders containing
    'darktable_exported' folders.
    """

    return folders


def readDT(fname):
    """
    Read a specified darktable xml file and return the title and tags.
    """

    if not os.path.isfile(fname):
        title, tags = ('nofile', '')

    # open XML file and parse

    return (title, tags)


def main():
    """
    do the main things
    """

    args = getArgs()

    outf = open(args.outfile, 'w')

    outf.write('"location","title","tags"\n')

    folders = findFolders(args.searchdir)

    for folder in folders:
        files = glob.glob(folder + 'darktable_exported/*.jpg')

        for fname in files:
            if not os.path.isfile(fname):
                sys.stderr.write(fname + ' not found. Skipping.\n')
            outf.write(fname + ',"')
            iname = fname.split('darktable_exported/')[-1].split('.jpg')[0]
            title, tags = readDT(folder + iname + '.xmp')
            if title == 'nofile':
                title = iname
            outf.write('"' + title + '","')
            outf.write(tags + '"\n')

    # output file
    # directory to search
    # get tags, title, and location? (default: yes)


    # determine which files are in `darktable_exported` folders

    # loop over files in folders
    # find the metadata files for those, extract title, tags, and the (relative)
    # path

    # write out batch upload CSV file


if __name__ == "__main__":
    main()
