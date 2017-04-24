# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.filemanager.destinations import FileDestinations

class AutoprintPlugin(octoprint.plugin.SettingsPlugin, 
						octoprint.plugin.TemplatePlugin,
						octoprint.plugin.EventHandlerPlugin):

	def get_settings_defaults(self):
		return dict(doprint=False)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
	]
	
	#this bit is from foosel's auto select plugin
	def on_event(self, event, payload):
		if event != "Upload":
			return

		if not self._printer.is_ready():
			self._logger.debug("Printer is not ready, not autoselecting uploaded file")
			return

		filename = payload["file"]
		target = payload["target"]

		if target == FileDestinations.SDCARD:
			path = filename
			sd = True
		else:
			path = self._file_manager.path_on_disk(target, filename)
			sd = False

		self._logger.info("Automatically printing {}".format(filename))
		self._printer.select_file(path, sd, self._settings.get(["doprint"])) #this line was modified to add the ability to also automatically print the uploaded file

__plugin_name__ = "Auto Print"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = AutoprintPlugin()
