"""
	Runs BotSK in a default configuration on a set of pages.

	Makes a backup of before-after contents.

	Should maybe later run more sk-like tasks.
	https://pl.wikipedia.org/wiki/Wikipedysta:Nux/wp_sk.js
"""

import pywikibot
from utils.file import *
from wpsk.Cleanup import *

import logging
logging.basicConfig(filename='logs/execute--sk.log', encoding='utf-8', level=logging.INFO)

# config
output_path = './io/execute--sk'

# init
site = pywikibot.Site('pl', 'wikipedia')
wpsk = Cleanup(site, output_path)

# init
Cleanup.initdir(output_path)

# real pages
"""
Getting pages from search results:
copy([...document.querySelectorAll('.mw-search-results a')].map(el=>el.href.replace(/^http.+\//, '')))
"""
pages = [
  "Ofiary_II_wojny_%C5%9Bwiatowej",
  "NXT_Cruiserweight_Championship",
]

# Loop over and make changes.
# Note that dryRun=True just loads a page and saves changes locally (to review changes before running)
for page_title in pages:
 	wpsk.fix_page(page_title, dryRun=True)
 	# wpsk.fix_page(page_title, dryRun=False)
