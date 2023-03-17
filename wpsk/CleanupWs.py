from wpsk.Cleanup import Cleanup

import pywikibot
from mwparserfromhell.wikicode import Wikicode

# Cleanup with Wikipedia specifc parts disabled.
class CleanupWs(Cleanup):
	def __init__(self,
		site: pywikibot.BaseSite,
		output_path: str
	):
		super().__init__(site, output_path)
		self.run_parser_fixes = False
		# description of change prefix (desc added in summary)
		self.desc_prefix = 'BeepBeep:'

	def _can_fix_tpls(self,
		page_code: Wikicode,
	):
		return False

	def _can_fix_text(self,
		page_code: Wikicode,
	):
		return False
