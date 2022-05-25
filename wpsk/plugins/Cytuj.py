"""
	Korekty szablonu Cytuj.

	See also:
	https://mwparserfromhell.readthedocs.io/en/latest/api/mwparserfromhell.nodes.html#module-mwparserfromhell.nodes.template
"""

import mwparserfromhell
from utils.file import *
import logging

# config
output_path = './io/lang-fix'
test_page_title = 'Wikipedysta:Nux/test_Cytuj_język'
desc_prefix = 'MiniSK: Poprawiam język w szablonach cytuj'

class Cytuj:
	def fix_lang(template: mwparserfromhell.nodes.template.Template) -> bool:
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
		return modified
