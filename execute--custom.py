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

def extra_change(page_text: str, summary: list):
	change_count = 0
	base_tpl_name = '(Zapaśnicy [^ ]+ na igrzyskach olimpijskich)'
	if re.search(base_tpl_name + r' - ', page_text) != None:
		page_text = re.sub(base_tpl_name + " - ", r"\1 – ", page_text)
		summary.append('sz-int')
		change_count = 1
		return (change_count, page_text)
	return (0, "")

wpsk.extra_changes.append(extra_change)
##

# real pages
"""
Getting pages from search results:
copy([...document.querySelectorAll('.mw-search-results a')].map(el=>el.href.replace(/^http.+\//, '')))
Getting pages from linked specila page:
copy(Array.from(document.querySelectorAll('#mw-whatlinkshere-list li > a')).map(el=>el.textContent))
"""
pages = [
	"Imre Szalay",
	"László Papp (zapaśnik)",
]
from lists.zapasnicy import pages as pages_lists
for pages in pages_lists:
	print (pages)
	for page_title in pages:
		# wpsk.fix_page(page_title, dryRun=True)
		wpsk.fix_page(page_title, dryRun=False)
	# break
