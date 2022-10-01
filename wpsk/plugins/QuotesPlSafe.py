"""
	Korekty polskich cudzysłowów.
"""

import mwparserfromhell
from mwparserfromhell.nodes.text import Text
from mwparserfromhell.wikicode import Wikicode
import re
import logging
from enum import Enum

from wpsk.plugins.QuotesPl import QuotesPl

class QuotesPlSafe(QuotesPl):
	def can_run_code(code: Wikicode) -> bool:
		"""
		Spr. czy są jakieś cudzysłowy do zmiany.
		"""
		text:str = str(code)
		# no tables/tags with quoted attribute values
		return text.count('="') < 1 and text.count('"') >= 2
