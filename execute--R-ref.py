"""
	R to ref with a BotSK.

	Kategoria techniczna:
	[[Kategoria:Nieobsługiwana nazwa przypisu R]]
	
	Makes a backup of before-after contents.

	VSC run: F5.
"""

import pywikibot
from utils.file import *
from wpsk.Cleanup import *

import logging
logging.basicConfig(filename='logs/execute--r-ref.log', encoding='utf-8', level=logging.INFO)

# config
output_path = './io/execute--r-ref'

# init
site = pywikibot.Site('pl', 'wikipedia')
wpsk = Cleanup(site, output_path)

# init
Cleanup.initdir(output_path)

##
# extra setup
##
wpsk.min_fix_count = 2

# change config
change_summary = 'Nieprawidłowe wywołania R:liczba'

# change
check_pattern = re.compile(r'\{\{[rR][^}]*\|:[0-9]+[|}]')
ref_pattern = re.compile(r'\{\{[rR]\s*\|\s*([^}="<>]+)\}\}')
def replace_match(match):
    names = match.group(1).split('|')
    replacement = ''.join(f'<ref name="{name}"/>' for name in names)
    return replacement
def extra_change(page_text: str, summary: list):
	if check_pattern.search(page_text):
		change_count = 0
		(page_text, change_count) = ref_pattern.subn(replace_match, page_text)
		if change_count >= 1:
			summary.append(change_summary)
			return (change_count * 2, page_text)
	return (0, "")

wpsk.extra_changes.append(extra_change)
##

##
# Running changes
from lists.cat_dump_list import pages as pages_lists

for pages in pages_lists:
	for page_title in pages:
		# wpsk.fix_page(page_title, dryRun=True)
		wpsk.fix_page(page_title, dryRun=False)

