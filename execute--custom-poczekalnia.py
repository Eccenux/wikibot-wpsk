"""
	WikiSource: Custom change(s) with a BotSK.

	Makes a backup of before-after contents.

	VSC run: F5.
"""

import pywikibot
from utils.file import *
from wpsk.CleanupWs import CleanupWs as Cleanup

import os
os.makedirs("logs/ws/", exist_ok=True)

import logging
logging.basicConfig(filename='logs/ws/execute--custom.log', encoding='utf-8', level=logging.INFO)

# config
output_path = './io/ws/execute--custom'

# init
site = pywikibot.Site('pl', 'wikisource')
wpsk = Cleanup(site, output_path)

# init
Cleanup.initdir(output_path)

##
# extra setup
##
wpsk.min_fix_count = 1

# original name
change_before = [
	#r"(\{\{[eE]pub\}\})[ \t]*([\r\n]* ?\{\{([cC]ałość|[eE]pub))",
	r"(\{\{[eE]pub\}\})[ \t]*()",
]
change_regexs = []
for change_pattern in change_before:
	#change_regexs.append(re.compile(change_pattern, re.IGNORECASE))
	change_regexs.append(re.compile(change_pattern))

# change
def extra_change(page_text: str, summary: list):
	change_count = 0
	for change_re in change_regexs:
		(page_text, change_count_re) = change_re.subn(r"\1<br>\2", page_text)
		change_count += change_count_re
	if change_count >= 1:
		summary.append('epub fix')
		return (change_count, page_text)
	return (0, "")

wpsk.extra_changes.append(extra_change)
##

##
# Running changes
##

# list of ids
from lists.epub_fix_pages import pages as pageIds

# execute and check for duplicates
skipped = []
done_already = []
page_gen = site.load_pages_from_pageids(pageIds)
for page in page_gen:
	page_title = page.title()
	if page_title in done_already:
		print (f'Duplicate page: {page_title}')
		continue
	# changed = wpsk.fix_page(page_title, dryRun=True)
	changed = wpsk.fix_page(page_title, dryRun=False)
	if not changed:
		skipped.append(page_title)
	else:
		done_already.append(page_title)

print ("\n\nSkipped pages (unchanged or duplicates):")
print (skipped)
#"""

# test reading page titles from ids
"""
page_gen = site.load_pages_from_pageids(pageIds)
count = 0
for page in page_gen:
	print (page.title())
	count += 1
	if count > 5:
		break
#"""