"""
	Remove old Tech/News in my talk page.

	Keeps the last section, so the most recent tech news is preserved.

	Makes a backup of before-after contents.
	Should be idempotent.
"""

import pywikibot, re
from utils.file import *

import logging
logging.basicConfig(filename='logs/arch-talk-tech.log', encoding='utf-8', level=logging.INFO)

site = pywikibot.Site("pl", 'wikipedia')

# config
output_path = './io/arch-talk'
archPage = 'Dyskusja wikipedysty:Nux'

print ("Checking: " + archPage)
page = pywikibot.Page(site, archPage)
page_text = page.text

## clear dir
#import shutil
#shutil.rmtree(output_path, ignore_errors=True)

# init dir
import os
os.makedirs(output_path, exist_ok=True)

##
# page text ops
##
# up until April 2022, remove all
page_text = re.sub(r"== \[\[m:Special:MyLanguage/Tech/News/.+=\n[\s\S]+?(?=\n==)", r"", page_text)

# from April 2022, remove all but last
found = re.findall(r"== Wiadomości techniczne: [0-9]{4}-[0-9]{2} ==(?=\n)", page_text)
print("");
print("Sections found:", len(found));
print(found);
print("");
if len(found) > 1:
	sections_to_remove = found[:-1]
	print("Sections to remove:", len(sections_to_remove));
	print(sections_to_remove);
	def remove_old(matchobj):
		all =  matchobj.group(0)
		title =  matchobj.group(1)
		if title in sections_to_remove:
			return ""
		return all
	page_text = re.sub(r"(== Wiadomości techniczne: [0-9]{4}-[0-9]{2} ==)\n[\s\S]+?(?=\n==)", remove_old, page_text)

	# backup
	save_page_content(page, output_path, suffix="_before")

	# apply
	page.text = page_text

	# cmp
	save_page_content(page, output_path, suffix="_removed")

	# save with description
	page.save('Beep, beep, kasowanie tech news')
	print("Tech news removed (except last).")	
else:
	print("Nothing to remove yet.")