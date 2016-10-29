import logging
logger = logging.getLogger(__name__)

import globalPluginHandler
import ui

import addonHandler
addonHandler.initTranslation()

import api
import textInfos

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def script_announce_scope(self, gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		line_text = info.text
		if not line_text:
			ui.message(_("No text found"))
			return
		char, position = find_indent(line_text)
		if position == 0:
			ui.message(_("Not indented"))
			return
		for line in previous_lines(info):
			prev_line_text = line.text
			if not prev_line_text.strip():
				continue
			new_char, new_position = find_indent(prev_line_text)
			if new_position < position:
				if new_position == 0 or new_char == char:
					ui.message(prev_line_text)
					return


	__gestures = {
		"kb:NVDA+alt+s": "announce_scope",
	}

def find_indent(text):
	indent_chars = ('\t', ' ')
	first = text[0]
	if first not in indent_chars:
		return '', 0
	for position, char in enumerate(text):
		if char != first:
			return first, position

def previous_lines(textInfo):
	textInfo.collapse()
	res = textInfo.move(textInfos.UNIT_LINE, -1)
	while res != 0:
		textInfo.expand(textInfos.UNIT_LINE)
		yield textInfo
		textInfo.collapse()
		res = textInfo.move(textInfos.UNIT_LINE, -1)
