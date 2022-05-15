"""
	Korekty polskich cudzysłowów.
"""

# import mwparserfromhell
from mwparserfromhell.nodes.text import Text
import re
import logging

# config
output_path = './io/lang-fix'
test_page_title = 'Wikipedysta:Nux/test_Cytuj_język'
desc_prefix = 'MiniSK: Poprawiam język w szablonach cytuj'

class QuotesPl:
	def fix(text_node: Text) -> bool:
		"""
		Wykonuje korekty.
		"""
		modified = False
		value: str = text_node.value
		if re.search(r'"', value):
			value = re.sub(r'"(.*?)"', r'„\1”', value)
			print (value)
			modified = True
		if modified:
			text_node.value = value
		return modified
