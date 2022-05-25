"""
	Korekty polskich cudzysłowów.

	Problematyczne fragmenty:
		"[[Lorem ipsum]]" dolor sit amet, consectetur adipiscing elit. "'''Curabitur ultrices'''" tincidunt sapien
	W ramach `filter_text` pierwszy cudzysłów będzie w dwóch `text_node`.
	Dlatego pierwszy cudzysłów musi zmienić stan na otwarty (`States.OPEN`), a potem, po linku, trzeba otwrzyć w poprzednim fragmencie i zamknąć cudzysłów.

	Pomijanie szablonów:
		Problem jest też z szablonami. Nie można zmieniać nazw grafik wewnątrz szablonu. Np. w infoboksie:
			|grafika                    = "Chuveirão" na Caverna Timimina.jpg
		Analogicznie byłby problem ze wszelkimi zmianami tekstowymi np. zmiana minusa tutaj psuje adres grafiki:
			|grafika                    = 'One of the wards in the hospital at Scutari'. Wellcome M0007724 - restoration, cropped.jpg
	Gdyby w szablonie była grafika, to w jej opisie poprawka byłaby OK.
	Mozna by też wykrywać czy coś wygląda jak plik po rozserzeniu... Ale ryzyk w szablonach może być więcej (nazwy kodowe itp).
"""

import mwparserfromhell
from mwparserfromhell.nodes.text import Text
from mwparserfromhell.wikicode import Wikicode
import re
import logging
from enum import Enum

# config
output_path = './io/lang-fix'
test_page_title = 'Wikipedysta:Nux/test_Cytuj_język'
desc_prefix = 'MiniSK: Poprawiam język w szablonach cytuj'

class States(Enum):
	START = 1
	OPEN = 2


def rreplace(s: str, old: str, new: str, max: int) -> str:
	"""
		Replace `old` with `new` in `s` from the right.
		Use `max` to limit replacements.
	"""
	parts = s.rsplit(old, max)
	return new.join(parts)

class QuotesPl:
	def __init__(self, code: Wikicode):
		self._code = code

		# state (start -> open -> start)
		self._state = States.START
		self._prev_node = None
		
		# modifications count (counting as a numer of full quotes replacements)
		self._count :int = 0

	def summary(self) -> int:
		"""
		Get summary post execution.
		"""
		return f"Cudzysłowy ({self._count})"
	
	def count(self) -> int:
		"""
		Modifications count.
		Here counting as a numer of full quotes replacements.
		"""
		return self._count

	def fix(self, text_node: Text) -> bool:
		"""
		Wykonuje korekty.
		"""
		modified = False
		value: str = text_node.value
		count: int = value.count('"')

		# nothing to do
		if count == 0:
			return modified

		# closing previous
		# (need to change previous and 1st in current)
		if self._state == States.OPEN:
			self._prev_node.value = rreplace(self._prev_node.value, '"', '„', 1)
			# print ('pre:' + self._prev_node.value.strip())
			value = re.sub(r'"', r'”', value, 1)
			self._count += 1
			modified = True
			count -= 1
			self._state = States.START
			self._prev_node = None
		
		# opening quote, but not sure if there is an end
		if count == 1 and self._state == States.START:
			self._state = States.OPEN
			self._prev_node = text_node
		elif count > 1:
			(value, sub_count) = re.subn(r'"(.*?)"', r'„\1”', value)
			self._count += sub_count
			modified = True
			if value.count('"'):
				self._state = States.OPEN
				self._prev_node = text_node

		if modified:
			# print ('bef:' + text_node.value.strip())
			# print ('aft:' + value.strip())
			text_node.value = value
		return modified
