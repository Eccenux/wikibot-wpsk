"""
	Download whatlinkshere pages list (linkujące).
"""

import pywikibot, re
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

	# download & save
	generator = list_template_embedded(site, tpl, content=False)
	#generator = pywikibot.pagegenerators.RegexFilter.titlefilter(generator, r'^Night of the')
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
	save_list(pages, base_path, list_name, append = append)
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
	

"""
tpls = [
	"Zapaśnicy Węgier na igrzyskach olimpijskich – Amsterdam 1928",
	"Zapaśnicy Węgier na igrzyskach olimpijskich – Atlanta 1996",
	"Zapaśnicy Węgier na igrzyskach olimpijskich – Barcelona 1992",
]
"""
list_name = "zapasnicy.py"
from lists.zapasnicytpls import pages as tpls
append = False
for page_title in tpls:
	download(page_title, output_path, list_name, append = append)
	append = True

# add pages variable
file = make_safe_filename(list_name)
path = os.path.join(output_path, file)
with open(path, "r+", encoding='utf-8') as text_file:
	text_file.seek(0)
	text = text_file.read()
	text_file.seek(0)
	text_file.write("pages = [\n")
	text_file.write(text)
	text_file.write("\n]\n")
# download(tpls[0], output_path, list_name, append = False)
# download(tpls[1], output_path, list_name)
