"""
	Test for parsing tables with attributes.
"""
import mwparserfromhell
text = """
{| class="wikitable"
|-
! style="width:101px" | heading1
! style="width:102px" | heading2
|- data-test="whatever"
| style="width:201px" | testing
|}
""".strip()
code = mwparserfromhell.parse(text)
# code.filter_tags(matches=lambda node: node.tag == "table")
# print (code.get_tree())

for node in code.filter():
	if isinstance(node, mwparserfromhell.nodes.tag.Tag):
		print(f'\n[{node.__class__.__name__}]({node.tag})<{node.attributes}>\n"""\n', str(node), '\n"""')
	else:
		print(f'\n[{node.__class__.__name__}]\n"""\n', node, '\n"""')


"""
<table class="wikitable">
	<tr>
		<th style="width:101px">heading1</th>
		<th style="width:102px">heading2</th>
	</tr>
	<tr data-test="whatever">
		<td style="width:201px">testing</td>
	</tr>
</table>
"""