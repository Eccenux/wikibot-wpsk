"""
	Download transcluded pages list (dołączone szbalony).
"""

import pywikibot, re
from pywikibot.pagegenerators import RegexFilter
from utils.api import *
from utils.file import *

import logging
logging.basicConfig(filename='logs/poczekalnia-list-links.log', encoding='utf-8', level=logging.DEBUG)

site = pywikibot.Site("pl", 'wikipedia')
output_path = './lists/'
limit = -1
#limit = 5

## clear dir
#import shutil
#shutil.rmtree(output_path, ignore_errors=True)

# init dir
import os

# """
tpls = [
	# "Wikipedia:Poczekalnia/artykuły",
	# "Wikipedia:Poczekalnia/biografie",
	# "Wikipedia:Poczekalnia/kwestie techniczne",
	"Wikipedia:Poczekalnia/reanimacja",
	# "Wikipedia:Poczekalnia/kwestie techniczne załatwione 24",
	# "Wikipedia:Poczekalnia/biografie załatwione 24",
	# "Wikipedia:Poczekalnia/artykuły załatwione 24",
]
#"""


# download list of transcluded page (templates)
def download(page_title, base_path, list_name, append = True):
	print('\nPage:', page_title)
	logging.info('\n\tPage: %s', page_title)

	os.makedirs(base_path, exist_ok=True)

	# template inclusions
	# generator = list_template_embedded(site, page_title, content=False)

	tpl_page = pywikibot.Page(site, page_title)
	generatorLinks = tpl_page.itertemplates()
	# generator = generatorLinks
	# only pages matching this
	generator = RegexFilter.titlefilter(generatorLinks, r'^Wikipedia:Poczekalnia/.+/202[34]\:', quantifier='all', ignore_namespace=False)

	# download & save
	counter = 0
	errors = 0
	# pages = [tpl_page.title()]	# include self
	pages = []
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
	Page: {page_title},
	Pages count: {counter},
	Errors count: {errors}.
	""".format_map({
		'counter': str(counter),
		'errors': str(errors),
		'page_title': page_title,
	})
	print(summary)
	logging.info(summary)
	


list_name = "poczekalnia_links.py"
# from lists.poczekalnia_tpls import pages as tpls

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
