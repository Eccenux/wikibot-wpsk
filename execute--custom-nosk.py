"""
	Custom change(s) without BotSK.

	Makes a backup of before-after contents.

	VSC run: F5.
"""

import pywikibot
from utils.file import *
from wpsk.CleanupWs import CleanupWs as Cleanup

import os
os.makedirs("logs/", exist_ok=True)

import logging
logging.basicConfig(filename='logs/execute--custom-nosk.log', encoding='utf-8', level=logging.INFO)

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
# Execute change (match and change)...
def extra_change(page_text: str, summary: list):
	change_count = 0

	##
	# xtools
	##
	# summary_text = 'supercount/xtools url'
	# (page_text, change_count_re) = re.subn(
	# 	r'https?://tools\.wmflabs\.org/supercount/(?:index\.php)?\?user=([^&]+)&project=([a-z]+\.wiki[pm]edia)(&[a-z0-9=&]+)?',
	# 	r'https://xtools.wmcloud.org/ec/\2/\1',
	# 	page_text
	# )
	# change_count += change_count_re
	# (page_text, change_count_re) = re.subn(
	# 	r'http://tools\.wmflabs\.org/xtools/pages/(?:index\.php)?\?user=([^&]+)&lang=pl&wiki=wikipedia&namespace=0&getall=1&redirects=noredirects',
	# 	r'https://xtools.wmcloud.org/pages/pl.wikipedia.org/\1',
	# 	page_text
	# )
	# change_count += change_count_re

	##
	# Szablony konkursowe cleanup
	##
	# summary_text = 'porządki [[Szablon:Wydarzenia]]'
	# "Wikipedysta:XaxeLoled/Szablony konkursowe/Konkurs 10" została przeniesiona do "Szablon:Wydarzenia/Miesiąc Wyróżnionego Artykułu 2022".
	# search:
	# https://pl.wikipedia.org/w/index.php?search=hastemplate%3A%22Wikipedysta%3AXaxeLoled%2FSzablony+konkursowe%2FKonkurs+10%22&title=Specjalna:Szukaj&profile=advanced&fulltext=1&advancedSearch-current=%7B%22fields%22%3A%7B%22hastemplate%22%3A%5B%22Wikipedysta%3AXaxeLoled%2FSzablony+konkursowe%2FKonkurs+10%22%5D%7D%7D&ns4=1
	# (page_text, change_count_re) = re.subn(r"\{Wikipedysta:XaxeLoled\/Szablony konkursowe\/Konkurs 10", r"{Wydarzenia/Miesiąc Wyróżnionego Artykułu 2022", page_text)
	# change_count += change_count_re

	# (page_text, change_count_re) = re.subn(r"\{Wikipedysta:XaxeLoled\/Szablony konkursowe\/Konkurs 9", r"{Wydarzenia/Wikiolimpiada 2022", page_text)
	# change_count += change_count_re

	# (page_text, change_count_re) = re.subn(r"\{Wikipedysta:XaxeLoled\/Szablony konkursowe\/Konkurs 11", r"{Wydarzenia/Święta 2022", page_text)
	# change_count += change_count_re

	# Wikipedysta:XaxeLoled/Szablony konkursowe/Konkurs 8
	# Szablon:Wydarzenia/CEE Spring 2022
	# (page_text, change_count_re) = re.subn(r"\{Wikipedysta:XaxeLoled\/Szablony konkursowe\/Konkurs 8", r"{Wydarzenia/Wydarzenia/CEE Spring 2022", page_text)
	# change_count += change_count_re

	# ["Wikipedysta:XaxeLoled/Szablony konkursowe"]
	# (page_text, change_count_re) = re.subn(r"/Konkurs 10", r"Szablon:Wydarzenia/Miesiąc Wyróżnionego Artykułu 2022", page_text)
	# change_count += change_count_re
	# (page_text, change_count_re) = re.subn(r"/Konkurs 9", r"Szablon:Wydarzenia/Wikiolimpiada 2022", page_text)
	# change_count += change_count_re
	# (page_text, change_count_re) = re.subn(r"/Konkurs 11", r"Szablon:Wydarzenia/Święta 2022", page_text)
	# change_count += change_count_re
	# (page_text, change_count_re) = re.subn(r"/Konkurs 8", r"Szablon:Wydarzenia/Wydarzenia/CEE Spring 2022", page_text)
	# change_count += change_count_re

	##
	# Migracja na nowy [[szablon:CW/weryfikacja]].
	##
	summary_text = 'Migracja na nowy [[szablon:CW/weryfikacja]].'
	(page_text, change_count_re) = re.subn(
		r"\{\{Wikiprojekt:Czy wiesz/weryfikacja",
		"{{subst:CW/migracja",
		page_text
	)
	change_count += change_count_re

	if change_count >= 1:
		summary.append(summary_text)
		return (change_count, page_text)
	return (0, "")

wpsk.extra_changes.append(extra_change)
##

##
# Running changes
##

# list of ids
from lists.nosk_links import pages as pages_lists

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
