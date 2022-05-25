"""
	Korekty polskich cudzysłowów.

	To nie zadzaiała:
	"[[Lorem ipsum]]" dolor sit amet, consectetur adipiscing elit. "'''Curabitur ultrices'''" tincidunt sapien
	W ramach `filter_text` pierwszy cudzysłów będzie niezależny od drugiego. W efekcie jest zupełenie bezsensowny wynik:
	"[[Lorem ipsum]]„ dolor sit amet, consectetur adipiscing elit. ”'''Curabitur ultrices'''" tincidunt sapien

	Pomijanie szablonów:
		Problem jest też z szablonami. Nie można zmieniać nazw grafik wewnątrz szablonu. Np. w infoboksie:
			|grafika                    = "Chuveirão" na Caverna Timimina.jpg
		Analogicznie byłby problem ze wszelkimi zmianami tekstowymi np. zmiana minusa tutaj psuje adres grafiki:
			|grafika                    = 'One of the wards in the hospital at Scutari'. Wellcome M0007724 - restoration, cropped.jpg
	Gdyby w szablonie była grafika, to w jej opisie poprawka byłaby OK.
	Mozna by też wykrywać czy coś wygląda jak plik po rozserzeniu... Ale ryzyk w szablonach może być więcej (nazwy kodowe itp).
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
