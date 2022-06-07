"""
	Test for traversing code with a table or two.
"""
import mwparserfromhell
from mwparserfromhell.wikicode import Wikicode
from mwparserfromhell.nodes import (
    Argument,
    Comment,
    ExternalLink,
    Heading,
    HTMLEntity,
    Node,
    Tag,
    Template,
    Text,
    Wikilink,
)

fileName = "test_parse_traversing_in.txt"
with open(fileName, 'r') as file:
	text = file.read()

code:Wikicode = mwparserfromhell.parse(text)
# code.filter_tags(matches=lambda node: node.tag == "table")
# print (code.get_tree())

# # loop over top level nodes
# for node in list(code.ifilter(recursive=False)):
# 	if isinstance(node, mwparserfromhell.nodes.tag.Tag):
# 		print(f'[{node.__class__.__name__}]({node.tag})<{node.attributes}>:', str(node).strip()[:10])
# 	else:
# 		print(f'[{node.__class__.__name__}]:', str(node).strip()[:10])

# recursive loop
def traverse_text(root, level = 0):
	# for debugging
	rootName = root.__class__.__name__

	if isinstance(root, Wikicode):
		children = list(root.ifilter(recursive=False))
	else:
		# children is the only thing that works
		# https://mwparserfromhell.readthedocs.io/en/latest/_modules/mwparserfromhell/nodes/_base.html#Node
		children = root.__children__()

	prefix = '  ' * level
	for node in children:
		nodeName = node.__class__.__name__

		if nodeName == 'Text':
			print(f'{prefix}[{nodeName}]({len(str(node))}):', str(node).strip()[:10])
		elif nodeName == 'Template':
			print(f'{prefix}[{nodeName}] - skip.')
		elif nodeName == 'Tag':
			print(f'{prefix}[{nodeName}]({node.tag})<{node.attributes}>')
			traverse_text(node, level+1)
		else:
			print(f'{prefix}[{nodeName}]({len(str(node))}) - dive into...')
			traverse_text(node, level+1)

traverse_text(code)