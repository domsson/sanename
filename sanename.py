#!/usr/bin/env python3
# coding: utf-8

# Author : Julien 'domsson' Dau
# Date   : 2018-12-05
# License: Public Domain (CC0)

# This script takes a directory path and turns all filenames within that 
# directory into what I consider 'sane': all lowercase, and almost only 
# alphanumeric characters (0-9, a-z), plus a few allowed characters.

import sys
import os
import re

#
# globals
#

OPT_KEEP_WHEN_HEAD = 1
OPT_KEEP_WHEN_BODY = 2
OPT_KEEP_WHEN_TAIL = 4

wordsep = "-"

# For a rationale as to what characters are allowed/removed, see the follwing
# link. We also remove the tilde because of its 'current dir' meaning in UNIX
# https://stackoverflow.com/questions/695438/safe-characters-for-friendly-url

allowed = ["-", "_", ".",]

# TODO: what do we do with "&", "+", "," and maybe ";"?

charmap = {
	"á": "a",
	"à": "a",
	"â": "a",
	"ǎ": "a",
	"ă": "a",
	"ä": "ae",
	"ã": "a",
	"é": "e",
	"è": "e",
	"ê": "e",
	"ě": "e",
	"ĕ": "e",
	"ë": "e",
	"í": "i",
	"ì": "i",
	"î": "i",
	"ǐ": "i",
	"ĭ": "i",
	"ï": "i",
	"ó": "o",
	"ò": "o",
	"ô": "o",
	"ǒ": "o",
	"ö": "oe",
	"õ": "o",
	"ø": "o",
	"ɵ": "o",
	"ú": "u",
	"ù": "u",
	"û": "u",
	"ǔ": "u",
	"ŭ": "u",
	"ü": "ue",
	"ñ": "n",
	"ý": "y",
	"ÿ": "y",
        "ẞ": "ss",
        "ß": "ss"
}

#
# functions
#

def make_sane(string, charmap={}, keep=[]):
    sane = []
    opts = 0

    # split the input string on whitespace
    tokens = string.split()

    # sanitize every word
    for i, token in enumerate(tokens):
        # for the first word: keep dots and similar in the beginning and middle 
        if i == 0: 
            opts = OPT_KEEP_WHEN_HEAD | OPT_KEEP_WHEN_BODY
        # for any other word: keep dots and similar only in the middle
        else:
            opts = OPT_KEEP_WHEN_BODY

        sane.append(make_sane_token(token, charmap, keep, opts))

    # join all words and return the string
    return wordsep.join(sane)


def make_sane_token(string, charmap={}, keep=[], opts=0):
    # Turn to lower case and remove leading/trailing whitespace
    string = string.lower().strip()

    # Now we swap some characters as specified in charmap
    for search, replace in charmap.items():
        string = string.replace(search, replace)
    
    # Now we remove everything not alpha-numeric and not in keep
    result = ""
    for i, c in enumerate(string):
        # keep chars from 'keep', if options allow it
        if c in keep:
            if i == 0:
                if opts & OPT_KEEP_WHEN_HEAD:
                    result += c
                continue
            if i == (len(string)-1):
                if opts & OPT_KEEP_WHEN_TAIL:
                    result += c
                continue
            if (opts & OPT_KEEP_WHEN_BODY):
                result += c
            continue
        # keep 0-9
        if ord(c) >= 48 and ord(c) <= 57:
            result += c
            continue
        # keep a-z
        if ord(c) >= 97 and ord(c) <= 122: 
            result += c
            continue
       
    # Done, return it!
    return result

#
# usage
#

if len(sys.argv) < 2:
	print("Usage: " + sys.argv[0] + " path/to/directory")
	sys.exit()
	
#
# main
#

# get the absolute path (we need that for os.replace())
path = os.path.abspath(sys.argv[1])

'''	
shift = ""
if len(sys.argv) > 2:
	shift = sys.argv[2].lower()
	print("Will remove " + shift + " from the beginning of file names.")

pop = ""
if len(sys.argv) > 3:
	pop = sys.argv[3].lower()
	print("Will remove " + pop + " from the end of file names.")
'''

# check if the given path is actually a directory
if not os.path.isdir(path):
	print("Error: not a directory: " + path)
	sys.exit()

# get all items in the directory as dir-entry iterator
dir_iter = os.scandir(path)

# prepare the list of files we want to work on
files = []

# go through all items in the directory (can include other directories)
for entry in dir_iter:
	# check if it is actually a file, not dir or symlink
	if entry.is_file():
		# add this to our list of files
		files.append(entry)

# see how many files we've found
num_files = len(files)

# if we haven't found any files? bye-bye
if num_files is 0:
	print("Error: directory has no files: " + path)
	sys.exit()

# check if the user really wants to press on
prompt = "About to rename " + str(num_files) + " files. Continue? (y/n) "
confirm = input(prompt).lower().strip()

if confirm == "n" or confirm == "no":
	print("Aborting")
	sys.exit()

# perfom the actual renaming!
for f in files:
        '''
	if new_name.startswith(shift):
		new_name = new_name[len(shift):]
	#if new_name.endswith(pop):
	#	new_name = new_name[:len(new_name)-len(pop)]
	'''
        file_name, file_ext = os.path.splitext(f.name)
        sane_name = make_sane(file_name, charmap, allowed)
        sane_ext  = file_ext.lower()
        sane_file = sane_name + sane_ext
        #print(f.name + " => " + sane_file)

        # TODO what's the diff between rename() and replace()?
        os.rename(f.path, os.path.join(path, sane_file))
        #os.replace(f.path, os.path.join(path, sane_file))

# close our resources
dir_iter.close()

# report success and bye-bye
print("Done, renamed " + str(num_files) + " files.")
sys.exit()
