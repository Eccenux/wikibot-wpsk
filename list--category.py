"""
	Download category pages list.
"""

import pywikibot, re
from utils.api import *
from utils.file import *

import logging
logging.basicConfig(filename='logs/list-cat.log', encoding='utf-8', level=logging.DEBUG)

site = pywikibot.Site("pl", 'wikipedia')
output_path = './io/lists/'
limit = -1
#limit = 5

## clear dir
#import shutil
#shutil.rmtree(output_path, ignore_errors=True)

# init dir
import os

def download(category, base_path, list_name, append = True):
	print('\nCategory:', category)
	logging.info('\n\tCategory: %s', category)

	os.makedirs(base_path, exist_ok=True)

	# download & save
	catPage = pywikibot.Category(site, category)
	# generator = catPage.articles(namespaces=[10])	# tpls only
	generator = catPage.articles(namespaces=[0])	# main only
	counter = 0
	errors = 0
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
	Category: {category},
	Pages count: {counter},
	Errors count: {errors}.
	""".format_map({
		'counter': str(counter),
		'errors': str(errors),
		'category': category,
	})
	print(summary)
	logging.info(summary)
	

# """
categories = [
	# "Kategoria:Szablony nawigacyjne - zapasy na igrzyskach olimpijskich",
	"Kategoria:Nieobsługiwana nazwa przypisu R",
]
#"""

# list_name = "zapasnicy_tpls_all.py"
list_name = "cat_dump_list.py"

# """
append = False
for page_title in categories:
	download(page_title, output_path, list_name, append = append)
	append = True
#"""
# download(categories[0], output_path, list_name, append = False)
# download(categories[1], output_path, list_name)

# add pages variable
save_list_var(output_path, list_name, var_name = 'pages')
