"""
	Runs BotSK on a test page.

	Makes a backup of before-after contents so you cna review it.
"""

import pywikibot
from utils.file import *
from wpsk.Cleanup import *

import logging
logging.basicConfig(filename='logs/execute--test.log', encoding='utf-8', level=logging.INFO)

# config
output_path = './io/execute--test'
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
