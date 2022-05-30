import mwparserfromhell
from mwparserfromhell.nodes.text import Text
from mwparserfromhell.nodes.template import Template
from mwparserfromhell.wikicode import Wikicode
import re
import logging

class BasePlugin:
	"""
	Base plugin class for BotSK.

	There should be one plugin instance per page so that counting modifications makes sense.
	But, mostly for testing, plugins should be able to work on smaller code fragments as well.
	"""

	def __init__(self, code: Wikicode, summary: str):
		# full code we are working on
		self._code = code
		# modifications count
		self._count :int = 0

		# Short text for summary
		self.i18nSummary = summary

	def summary(self) -> str:
		"""
		Get summary post execution.
		"""
		return f"{self.i18nSummary} ({self._count})"
	
	def count(self) -> int:
		"""
		Modifications count.

		Number can be specifc to a plugin.
		This can mean number of nodes added (e.g. templates).
		It could mean number of characters added or modified (but that would mostly be hard to count and quantify).
		"""
		return self._count

	def can_run(self) -> bool:
		"""
		Checks if there is a chance that a run method will modify code.

		This SHOULD give an estimate in some plugins (when exact check is expensive).
		"""
		return self.can_run_code(self._code)

	def can_run_code(code: Wikicode) -> bool:
		"""
		A static alias of `can_run`.
		"""
		return True

	"""
	def run(self, node: Text) -> bool:
		modified = False
		value: str = node.value
		
		if modified:
			# print ('bef:' + node.value.strip())
			# print ('aft:' + value.strip())
			node.value = value

		return modified
	"""
