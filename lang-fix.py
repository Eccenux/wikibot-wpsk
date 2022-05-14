'''
	Naprawia parametr język w szablonie Cytuj.

	Makes a backup of before-after contents.

	Should maybe later run more sk-like tasks.
'''

from sre_parse import parse_template
import pywikibot, re
import mwparserfromhell
from utils.file import *

import logging
logging.basicConfig(filename='logs/lang-fix.log', encoding='utf-8', level=logging.INFO)

site = pywikibot.Site('pl', 'wikipedia')

# config
output_path = './io/lang-fix'
test_page_title = 'Wikipedysta:Nux/test_Cytuj_język'
desc_prefix = 'MiniSK: Poprawiam język w szablonach cytuj'

def initdir(dir_path, clear=False):
	logging.info('Preapre dir: %s', dir_path)

	if clear:
		# clear dir
		import shutil
		shutil.rmtree(dir_path, ignore_errors=True)

	# init dir
	import os
	os.makedirs(dir_path, exist_ok=True)

def fix_lang(template: mwparserfromhell.nodes.template.Template) -> bool:
	lang_param = 'język'
	tpl_name = str(template.name).strip().lower()
	modified = False
	if tpl_name.startswith('cytuj') and template.has(lang_param):
		logging.info('Template: %s', tpl_name)
		lang = template.get(lang_param).value.strip()
		if lang == 'pl' or lang.startswith('pl-'):
			template.remove(lang_param)
			logging.info('\tremoved: %s', lang)
			modified = True
		if lang.startswith('en-'):
			template.add(lang_param, 'en')
			logging.info('\treplaced: %s', lang)
			modified = True
	return modified

def fix_page(page_title: str):
	# read content
	logging.info ('Checking: ' + page_title)
	print ('Checking: ' + page_title)
	page = pywikibot.Page(site, page_title)
	page_text: str = page.text
	page_code: mwparserfromhell.wikicode.Wikicode = mwparserfromhell.parse(page_text)

	# find templates with param
	# https://mwparserfromhell.readthedocs.io/en/latest/api/mwparserfromhell.nodes.html#module-mwparserfromhell.nodes.template
	fix_count_lang = 0
	for template in page_code.filter_templates():
		# before = str(template)
		modified = fix_lang(template)
		if modified:
			fix_count_lang += 1
			# after = str(template)
			# print(f'b: {before}\na: {after}')

	page_text = str(page_code)
	if (page_text.strip() == page.text.strip()):
		logging.info('Nothing to do.')
		print ('Nothing to do.')
	else:
		# backup
		save_page_content(page, output_path, suffix='_before')

		# apply
		page.text = page_text

		# cmp
		save_page_content(page, output_path, suffix='_removed')

		# save with description
		desc = f'{desc_prefix} ({fix_count_lang}).'
		logging.info(f'Save "{page.title()}"\n{desc}')
		print(f'Save "{page.title()}"\n{desc}')
		#page.save()

# exec
initdir(output_path)
fix_page(test_page_title)