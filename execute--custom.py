"""
	Custom change(s) with a BotSK.

	Makes a backup of before-after contents.

	VSC run: F5.
"""

import pywikibot
from utils.file import *
from wpsk.Cleanup import *

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

# Judocy Austrii na igrzyskach olimpijskich - Ateny 2004
# Judocy Austrii na IGRZYSKACH OLIMPIJSKICH – Ateny 2004
# Zapaśnicy Wielkiej Brytanii na Igrzyskach Olimpijskich – Atlanta 1996
change_pattern = re.compile(r"([\wzażółćgęśląjaźń]+ [^}\[\]\n]+ na) igrzyskach olimpijskich [–-] ", re.IGNORECASE)
def extra_change(page_text: str, summary: list):
	(page_text, change_count) = change_pattern.subn(r"\1 igrzyskach olimpijskich – ", page_text)
	if change_count >= 1:
		summary.append('sz-nazwa')
		return (change_count, page_text)
	return (0, "")

wpsk.extra_changes.append(extra_change)
##

##
# Running changes
##
"""
Getting pages from search results:
copy([...document.querySelectorAll('.mw-search-results a')].map(el=>el.href.replace(/^http.+\//, '')))
Getting pages from linked specila page:
copy(Array.from(document.querySelectorAll('#mw-whatlinkshere-list li > a')).map(el=>el.textContent))
"""
# small scale changes
"""
pages = [
	"Imre Szalay",
	"László Papp (zapaśnik)",
]
for page_title in pages:
	wpsk.fix_page(page_title, dryRun=True)
"""
# list of lists
from lists.sportowcy_io_links import pages as pages_lists
skipped = []
done_already = []
for pages in pages_lists:
	#print (pages)
	for page_title in pages:
		if page_title in done_already:
			print (f'Duplicate page: {page_title}')
			continue
		# changed = wpsk.fix_page(page_title, dryRun=True)
		changed = wpsk.fix_page(page_title, dryRun=False)
		if not changed:
			skipped.append(page_title)
		else:
			done_already.append(page_title)
	# break
print ("\n\nSkipped pages (unchanged or duplicates):")
print (skipped)
#"""
