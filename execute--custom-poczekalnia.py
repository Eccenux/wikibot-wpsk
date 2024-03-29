"""
	Custom change(s) without the BotSK.

	Makes a backup of before-after contents.

	VSC run: F5.
"""

import pywikibot
from utils.file import *
from wpsk.CleanupWs import CleanupWs as Cleanup

import os
os.makedirs("logs/", exist_ok=True)

import logging
logging.basicConfig(filename='logs/execute--custom.log', encoding='utf-8', level=logging.INFO)

# config
output_path = './io/execute--custom'

# init
site = pywikibot.Site('pl', 'wikipedia')
wpsk = Cleanup(site, output_path)

# init
Cleanup.initdir(output_path)

##
# extra setup
##
wpsk.min_fix_count = 1

##
# changes spec
##
change_regexs = [
	{
		"re": re.compile(r"(\{\{[lL]nDNU\|[^}]+)\|\s*strona=[^}|]+([^}]*\}\})"),
		"to": r"\1\2",
		"mul": 1,
	},
	{
		"re": re.compile(r"(\{\{[lL]nDNU\|[^}]+)\}\}"),
		"to": r"\1|strona={{subst:FULLPAGENAME}}}}",
		"mul": 1,
	},
]
# change
def extra_change(page_text: str, summary: list):
	change_count = 0
	for change in change_regexs:
		(page_text, change_count_re) = change['re'].subn(change['to'], page_text)
		change_count += change_count_re * change['mul']
	if change_count >= 1:
		summary.append('podstrona do lnDNU')
		return (change_count, page_text)
	return (0, "")

wpsk.extra_changes.append(extra_change)
##

##
# Running changes
##

# list of ids
from lists.poczekalnia_links import pages as pages_lists

# execute and check for duplicates
skipped = []
done_already = []
for pages in pages_lists:
	#print (pages)
	for page_title in pages:
		if page_title in done_already:
			print (f'Duplicate page: {page_title}')
			continue
		changed = wpsk.fix_page(page_title, dryRun=True)
		# changed = wpsk.fix_page(page_title, dryRun=False)
		if not changed:
			skipped.append(page_title)
		else:
			done_already.append(page_title)

print ("\n\nSkipped pages (unchanged or duplicates):")
print (skipped)
#"""
