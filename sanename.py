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

allowed = ["-", "_", "."]

charmap = {
	" ": "-",
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
}

#
# functions
#

def make_sane(string, keep=[], charmap={}):
	# Turn lowercase, strip whitespace at beginning and end
	string = string.lower().strip()
	# Now we swap some characters as specified in charmap
	for search, replace in charmap.items():
		string = string.replace(search, replace)
	# Now we remove everything not alpha-numeric and not in keep
	result = ""
	for i, c in enumerate(string):
		if c in keep: # allowed characters
			result += c
			continue
		if ord(c) >= 48 and ord(c) <= 57: # 0-9
			result += c
			continue
		if ord(c) >= 97 and ord(c) <= 122: # a-z
			result += c
			continue
		if ord(c) >= 65 and ord(c) <= 90: # A-Z -> a-z
			result += chr(ord(c) + 32)
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

shift = ""
if len(sys.argv) > 2:
	shift = sys.argv[2].lower()
	print("Will remove " + shift + " from the beginning of file names.")

'''	
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
	print("Error: directory empty: " + path)
	sys.exit()

# check if the user really wants to press on
prompt = "About to rename " + str(num_files) + " files. Continue? (y/n) "
confirm = input(prompt).lower().strip()

if confirm == "n" or confirm == "no":
	print("Aborting")
	sys.exit()

# perfom the actual renaming!
for f in files:
	new_name = make_sane(f.name, allowed, charmap)
	if new_name.startswith(shift):
		new_name = new_name[len(shift):]
	#if new_name.endswith(pop):
	#	new_name = new_name[:len(new_name)-len(pop)]
	#print(new_name)	
	os.rename(f.path, os.path.join(path, new_name))

# close our resources
dir_iter.close()

# report success and bye-bye
print("Done, renamed " + str(num_files) + " files.")
sys.exit()
