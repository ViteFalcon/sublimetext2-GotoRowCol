import sublime, sublime_plugin


class PromptGotoRowColCommand(sublime_plugin.WindowCommand):
	def run(self, automatic = True):
		self.window.show_input_panel(
			'Enter a row and a column',
			'1 1',
			self.gotoRowCol,
			None,
			None
		)
		pass

	def gotoRowCol(self, text):
		try:
			(row, col) = map(str, text.split(" "))

			if self.window.active_view():
				self.window.active_view().run_command(
					"goto_row_col",
					{"row": row, "col": col}
				)
		except ValueError:
			pass


class GotoRowColCommand(sublime_plugin.TextCommand):
	def run(self, edit, row, col):
		print "INFO: Input: " + str({"row": row, "col": col})
		# rows and columns are zero based, so subtract 1
		# convert text to int
		(row, col) = (int(row) - 1, int(col) - 1)
		if row > -1 and col > -1:
			# col may be greater than the row length
			col = min(col, len(self.view.substr(self.view.full_line(self.view.text_point(row, 0))))-1)
			print "INFO: Calculated: " + str({"row": row, "col": col})
			self.view.sel().clear()
			self.view.sel().add(sublime.Region(self.view.text_point(row, col)))
			self.view.show(self.view.text_point(row, col))
		else:
			print "ERROR: row or col are less than zero"