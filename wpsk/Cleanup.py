"""
	Base script for WP:SK cleanup.

	Makes a backup of before-after contents.

	Should eventually run more sk-like tasks.

	Use `extra_changes` property to add custom changes in wikicode string.
	Those function(s) are run after BotSK changes.
	# You change the text.
	# Append your info to summary.
	# And return 1 or higher as a count.
	def extra_change(
		page_text: str,
		summary: list,
	):
		return (change_count, page_text_new)
	Note! If change_count is 0 then changes are ignored. So you can do:
		return (0, "")
"""

import pywikibot
import mwparserfromhell
from mwparserfromhell.wikicode import Wikicode
from utils.file import *
from wpsk.plugins.Cytuj import Cytuj
from wpsk.plugins.QuotesPlSafe import QuotesPlSafe
import wpsk.perf as perf
import logging

class Cleanup:
	def __init__(self,
		site: pywikibot.BaseSite,
		output_path: str
	):
		self.site = site
		self.output_path = output_path
		# description of change prefix (desc added in summary)
		self.desc_prefix = 'BotSK:'
		# minimum number of changes for the change to be worth it
		self.min_fix_count = 2
		# array of additional changes (functions)
		self.extra_changes = []
		# run parser and standard fixes
		# (set to False to skip parsing the page and just run `extra_changes`)
		self.run_parser_fixes = True

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

		# standard fixes based on MWPFromHell.
		if self.run_parser_fixes:
			dt_start = perf.start()
			page_code: Wikicode = mwparserfromhell.parse(page_text)
			perf.check(dt_start, "parse page")

			# fix/change
			dt_start = perf.start()
			(fix_count, summary) = self._fix_code(page_code)
			perf.check(dt_start, "_fix_code")
			
			page_text = str(page_code)
		else:
			fix_count = 0
			summary = []

		# extra changes in wikicode
		for extra_change in self.extra_changes:
			(extra_count, page_text_new) = extra_change(page_text, summary)
			if extra_count>0:
				page_text = page_text_new
				fix_count += extra_count

		# minimum 2 changes required to apply modifications
		if fix_count >= self.min_fix_count:
			self._apply(page, page_text, summary, dryRun)
			return True
		else:
			logging.warning (f'Skipping, too little changes: {fix_count}.')
			print (f'Skipping, too little changes: {fix_count}.')
			return False

	def _fix_code(self,
		page_code: Wikicode,
	):
		fix_count = 0
		summary = []

		dt_start = perf.start()
		if self._can_fix_tpls(page_code):
			perf.check(dt_start, "_can_fix_tpls")
			dt_start = perf.start()
			fix_count += self._fix_tpls(page_code, summary)
			perf.check(dt_start, "_fix_tpls")
		dt_start = perf.start()
		if self._can_fix_text(page_code):
			perf.check(dt_start, "_can_fix_text")
			dt_start = perf.start()
			fix_count += self._fix_text(page_code, summary)
			perf.check(dt_start, "_fix_text")

		return (fix_count, summary)

	#region <TPL FIXES>
	def _can_fix_tpls(self,
		page_code: Wikicode,
	):
		plugins = [Cytuj]
		for plugin in plugins:
			if plugin.can_run_code(page_code):
				return True
		return False

	def _fix_tpls(self,
		page_code: Wikicode,
		summary: list,
	):
		fix_count = 0

		# templates
		cytuj = Cytuj(page_code)
		for template in page_code.filter_templates():
			cytuj.run(template)
		if cytuj.count() > 0:
			fix_count += cytuj.count()
			summary.append(cytuj.summary())
		
		return fix_count
	#endregion
	
	#region <TEXT FIXES>
	def _can_fix_text(self,
		page_code: Wikicode,
	):
		plugins = [QuotesPlSafe]
		for plugin in plugins:
			if plugin.can_run_code(page_code):
				return True
		return False

	def _fix_text(self,
		page_code: Wikicode,
		summary: list,
	):
		fix_count = 0

		# text
		quotesPl = QuotesPlSafe(page_code)
		for text_node in page_code.filter_text():
			# skip in templates (directly in templates)
			parent = page_code.get_parent(text_node)
			if isinstance(parent, mwparserfromhell.nodes.template.Template):
				continue
			quotesPl.run(text_node)
		if quotesPl.count() > 0:
			fix_count += quotesPl.count()
			summary.append(quotesPl.summary())
		
		return fix_count
	#endregion

	def _apply(self,
		page: pywikibot.Page,
		page_text: str,
		summary: list,
		dryRun: True,
	):
		"""
		:page should be unchanged at this point.
		:page_text contains a new value
		:summary is a list short(!) info on the changes of each plugin/function
		"""
		if (page_text.strip() == page.text.strip()):
			logging.info('Nothing to do.')
			print ('Nothing to do.')
		else:
			# backup
			save_page_content(page, self.output_path, suffix='_before')

			# apply
			page.text = page_text

			# cmp
			save_page_content(page, self.output_path, suffix='_modified')

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
