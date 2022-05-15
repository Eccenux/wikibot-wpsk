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
test_page_title = 'Wikipedysta:Nux/test_Cytuj_język'
desc_prefix = 'MiniSK: Poprawiam język w szablonach cytuj'

# init
site = pywikibot.Site('pl', 'wikipedia')
wpsk = Cleanup(site, output_path)

# exec
Cleanup.initdir(output_path)
wpsk.fix_page(test_page_title)
# copy([...document.querySelectorAll('.mw-search-results a')].map(el=>el.href.replace(/^http.+\//, '')))
# pages = [
#   "Spaso",
# ]
# for page_title in pages:
# 	fix_page(page_title, dryRun=True)
# 	#fix_page(page_title, dryRun=False)
