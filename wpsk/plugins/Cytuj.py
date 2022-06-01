"""
	Korekty szablonu Cytuj.

	See also:
	https://mwparserfromhell.readthedocs.io/en/latest/api/mwparserfromhell.nodes.html#module-mwparserfromhell.nodes.template
"""

import mwparserfromhell
from mwparserfromhell.nodes.template import Template
from mwparserfromhell.wikicode import Wikicode
from utils.file import *
import logging

from wpsk.plugins.BasePlugin import BasePlugin

class Cytuj(BasePlugin):
	def __init__(self, code: Wikicode):
		super().__init__(code, summary="Język w Cytuj*")

	def can_run_code(code: Wikicode) -> bool:
		"""
		Spr. czy są parametry do zmiany.
		"""
		return re.search(r'język\s*=\s*[a-z]+-', str(code)) != None
	
	def run(self, template: Template) -> bool:
		"""
		Naprawia parametr język w szablonach cytuj*.
		"""

		lang_param = 'język'
		tpl_name = str(template.name).strip().lower()
		modified = False
		if tpl_name.startswith('cytuj') and template.has(lang_param):
			logging.info('Template: %s', tpl_name)
			lang = template.get(lang_param).value.strip()
			dash = lang.find('-')
			if dash > 0:
				l = lang[0:dash]
				if l == 'pl' or l == 'en' or l == 'fr' or l == 'de':
					template.add(lang_param, l)
					logging.info('\treplaced: %s', lang)
					modified = True

		if modified:
			self._count += 1
			
		return modified
