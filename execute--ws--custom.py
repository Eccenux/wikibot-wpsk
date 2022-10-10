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
# change_pattern = re.compile(r"([\wzażółćgęśląjaźń]+ [^}\[\]\n]+ na) igrzyskach olimpijskich [–-] ", re.IGNORECASE)

# original name
change_before = [
	r"(Bokserzy Polski na Letnich Igrzyskach Olimpijskich) - (Atlanta 1996)",
	r"(Bokserzy Rosji na Letnich Igrzyskach Olimpijskich) - (Atlanta 1996)",
	r"(Bokserzy Rumunii na Letnich Igrzyskach Olimpijskich) - (Atlanta 1996)",
	r"(IO Australia 2020) - (kobiety)",
	r"(IO Belgia 2020) - (kobiety)",
	r"(IO Francja 2020) - (kobiety)",
	r"(IO Kanada 2020) - (kobiety)",
	r"(IO Serbia 2020) - (kobiety)",
	r"(IO USA 2020) - (kobiety)",
	r"(Mistrzowie olimpijscy w kombinacji norweskiej) - (duża skocznia)",
	r"(Piłka siatkowa na LIO 2012) - (kwalifikacje)",
]
change_regexs = []
for change_pattern in change_before:
	#change_regexs.append(re.compile(change_pattern, re.IGNORECASE))
	change_regexs.append(re.compile(change_pattern))

# change
def extra_change(page_text: str, summary: list):
	change_count = 0
	for change_re in change_regexs:
		(page_text, change_count_re) = change_re.subn(r"\1 – \2", page_text)
		change_count += change_count_re
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
Getting pages from linked special page:
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
from lists.other_io_links import pages as pages_lists
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
