"""
	Download whatlinkshere pages list (zagnieżdżone/użyte szablony, albo linkujące).
"""

import pywikibot, re
from pywikibot.pagegenerators import RegexFilter
from utils.api import *
from utils.file import *

import logging
logging.basicConfig(filename='logs/list-links.log', encoding='utf-8', level=logging.DEBUG)

site = pywikibot.Site("pl", 'wikipedia')
output_path = './io/lists/'
limit = -1
#limit = 5

## clear dir
#import shutil
#shutil.rmtree(output_path, ignore_errors=True)

# init dir
import os

def download(tpl, base_path, list_name, append = True):
	print('\nTemplate:', tpl)
	logging.info('\n\tTemplate: %s', tpl)

	os.makedirs(base_path, exist_ok=True)

	
	# template inclusions
	# generator = list_template_embedded(site, tpl, content=False)
	generator = list_template_embedded(site, tpl, content=False, namespaces=[0])

	# all links but filtered
	tpl_page = get_template_page(site, tpl)
	# generatorLinks = tpl_page.backlinks()
	# # skip technical/arch pages
	# generator = RegexFilter.titlefilter(generatorLinks, r'^(Wikiprojekt:Sprzątanie szablonów|Wikipedysta:PBbot)/', quantifier='none', ignore_namespace=False)

	# download & save
	counter = 0
	errors = 0
	pages = [tpl_page.title()]	# include self
	for page in generator:
		counter += 1
		try:
			# print(page.title())
			# logging.debug(page.title())
			pages.append(page.title())
			if limit > 0 and counter > limit:
				break
		except Exception as error:
			errors += 1
			logging.error({'page':page, 'error':error})
	save_list_data(pages, base_path, list_name, append = append)
	summary = """
	Template: {tpl},
	Pages count: {counter},
	Errors count: {errors}.
	""".format_map({
		'counter': str(counter),
		'errors': str(errors),
		'tpl': tpl,
	})
	print(summary)
	logging.info(summary)
	

# """
list_name = "bio_zima_links.py"
tpls = [
	"Zawodnik zima infobox",
	# "Zapaśnicy Węgier na igrzyskach olimpijskich – Atlanta 1996",
	# "Zapaśnicy Węgier na igrzyskach olimpijskich – Barcelona 1992",
]
#"""

# list_name = "other_io_links.py"
# from lists.other_io_tpls import pages as tpls

# """
append = False
for page_title in tpls:
	download(page_title, output_path, list_name, append = append)
	append = True
#"""
# download(tpls[0], output_path, list_name, append = False)
# download(tpls[1], output_path, list_name)

# add pages variable
save_list_var(output_path, list_name, var_name = 'pages')
