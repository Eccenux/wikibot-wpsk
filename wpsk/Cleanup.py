"""
	Base script for WP:SK cleanup.

	Makes a backup of before-after contents.

	Should eventually run more sk-like tasks.
"""

import pywikibot
import mwparserfromhell
from utils.file import *
from wpsk.plugins.Cytuj import Cytuj
import logging

class Cleanup:
	def __init__(self,
		site: pywikibot.BaseSite,
		output_path: str
	):
		self.site = site
		self.output_path = output_path
		self.desc_prefix = 'MiniSK: Poprawiam język w szablonach cytuj'

	def initdir(dir_path: str, clear=False):
		logging.info('Preapre dir: %s', dir_path)

		if clear:
			# clear dir
			import shutil
			shutil.rmtree(dir_path, ignore_errors=True)

		# init dir
		import os
		os.makedirs(dir_path, exist_ok=True)

	def fix_page(self, page_title: str, dryRun = True):
		# read content
		logging.info ('Checking: ' + page_title)
		print ('Checking: ' + page_title)
		page = pywikibot.Page(self.site, page_title)
		page_text: str = page.text
		page_code: mwparserfromhell.wikicode.Wikicode = mwparserfromhell.parse(page_text)

		# find templates with param
		# https://mwparserfromhell.readthedocs.io/en/latest/api/mwparserfromhell.nodes.html#module-mwparserfromhell.nodes.template
		fix_count_lang = 0
		for template in page_code.filter_templates():
			# before = str(template)
			modified = Cytuj.fix_lang(template)
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
			save_page_content(page, self.output_path, suffix='_before')

			# apply
			page.text = page_text

			# cmp
			save_page_content(page, self.output_path, suffix='_removed')

			# save with description
			desc = f'{self.desc_prefix} ({fix_count_lang}).'
			if dryRun:
				logging.info(f'Dry-Save "{page.title()}"\n{desc}')
				print(f'Dry-Save "{page.title()}"\n{desc}')
			else:
				logging.info(f'Save "{page.title()}"\n{desc}')
				print(f'Save "{page.title()}"\n{desc}')
				page.save(desc)
