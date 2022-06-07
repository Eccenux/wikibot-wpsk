"""
	Test for traversing code with a table or two.
"""
import mwparserfromhell
from mwparserfromhell.wikicode import Wikicode

fileName = "test_parse_traversing_in.txt"
with open(fileName, 'r') as file:
	text = file.read()

code:Wikicode = mwparserfromhell.parse(text)
# code.filter_tags(matches=lambda node: node.tag == "table")
# print (code.get_tree())

# loop over top level nodes
for node in list(code.ifilter(recursive=False)):
	if isinstance(node, mwparserfromhell.nodes.tag.Tag):
		print(f'[{node.__class__.__name__}]({node.tag})<{node.attributes}>:', str(node).strip()[:10])
	else:
		print(f'[{node.__class__.__name__}]:', str(node).strip()[:10])
