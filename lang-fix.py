"""
	Naprawia parametr język w szablonie Cytuj.

	Makes a backup of before-after contents.

	Should maybe later run more sk-like tasks.
	https://pl.wikipedia.org/wiki/Wikipedysta:Nux/wp_sk.js
"""

import pywikibot
from utils.file import *
from wpsk.Cleanup import *

import logging
logging.basicConfig(filename='logs/lang-fix.log', encoding='utf-8', level=logging.INFO)

# config
output_path = './io/lang-fix'
# test_page_title = 'Wikipedysta:Nux/test_Cytuj_język'
test_page_title = 'Wikipedysta:Nux/test quotePL/NXT Cruiserweight Championship'
# test_page_title = 'Wikipedysta:Nux/test quotePL/Ofiary II wojny'

# init
site = pywikibot.Site('pl', 'wikipedia')
wpsk = Cleanup(site, output_path)

# init
Cleanup.initdir(output_path)

# test
wpsk.fix_page(test_page_title, dryRun=True)

# real pages
"""
Getting pages from search results:
copy([...document.querySelectorAll('.mw-search-results a')].map(el=>el.href.replace(/^http.+\//, '')))
""
pages = [
  "Ofiary_II_wojny_%C5%9Bwiatowej",
  "NXT_Cruiserweight_Championship",
]
for page_title in pages:
 	wpsk.fix_page(page_title, dryRun=True)
 	# wpsk.fix_page(page_title, dryRun=False)
#"""