"""
	Base script for WP:SK cleanup.

	Makes a backup of before-after contents.

	Should eventually run more sk-like tasks.
"""

import pywikibot
import mwparserfromhell
from mwparserfromhell.wikicode import Wikicode
from utils.file import *
from wpsk.plugins.Cytuj import Cytuj
from wpsk.plugins.QuotesPl import QuotesPl
import logging

class Cleanup:
	def __init__(self,
		site: pywikibot.BaseSite,
		output_path: str
	):
		self.site = site
		self.output_path = output_path
		self.desc_prefix = 'MiniSK:'

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
		page_code: Wikicode = mwparserfromhell.parse(page_text)
		(fix_count, summary) = self._fix_code(page_code)
		if fix_count > 1:
			self._apply(page, page_code, summary, dryRun)

	def _fix_code(self,
		page_code: Wikicode,
	):
		# fixes by type
		fix_count = 0
		summary = []
		
		# templates
		fix_count_lang = 0
		for template in page_code.filter_templates():
			modified = Cytuj.fix_lang(template)
			if modified:
				fix_count_lang += 1
		if fix_count_lang > 0:
			fix_count += fix_count_lang
			summary.append(f'Język w Cytuj* ({fix_count_lang})')
		
		# text
		quotesPl = QuotesPl(page_code)
		for text_node in page_code.filter_text():
			# skip in templates (directly in templates)
			parent = page_code.get_parent(text_node)
			if isinstance(parent, mwparserfromhell.nodes.template.Template):
				continue
			quotesPl.fix(text_node)
		if quotesPl.count() > 0:
			fix_count += quotesPl.count()
			summary.append(quotesPl.summary())
		
		return (fix_count, summary)

	def _apply(self,
		page: pywikibot.Page,
		page_code: Wikicode,
		summary: list,
		dryRun: True,
	):
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

			# ~save
			self._save(page, summary, dryRun)

	def _save(self,
		page: pywikibot.Page,
		summary: list,
		dryRun: True,
	):
		# save with description
		desc = f'{self.desc_prefix} {", ".join(summary)}.'
		if dryRun:
			logging.info(f'Dry-Save "{page.title()}"\n{desc}')
			print(f'Dry-Save "{page.title()}"\n{desc}')
		else:
			logging.info(f'Save "{page.title()}"\n{desc}')
			print(f'Save "{page.title()}"\n{desc}')
			page.save(desc)
