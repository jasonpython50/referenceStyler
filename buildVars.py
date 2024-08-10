# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Since some strings in `addon_info` are translatable,
# we need to include them in the .po files.
# Gettext recognizes only strings given as parameters to the `_` function.
# To avoid initializing translations in this module we simply roll our own "fake" `_` function
# which returns whatever is given to it as an argument.
def _(arg):
	return arg

# Add-on information variables
addon_info = {
	# add-on Name/identifier, internal for NVDA
	"addon_name": "referenceStyler",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on
	# to be shown on installation and add-on information found in Add-ons Manager.
	"addon_summary": _("Reference Styler"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description": _("""This add-on allows users to manage and insert references in various citation styles.
It supports APA, MLA, Chicago, Vancouver, Harvard, IEEE, AMA, and ACS styles."""),
	# version
	"addon_version": "24.0.0",
	# Author(s)
	"addon_author": "Asamoah Emmanuel <emmanuelasamoah179@gmail.com>",
	# URL for the add-on documentation support
	"addon_url": "https://github.com/jasonpython50/referenceStyler",
	# URL for the add-on repository where the source code can be found
	"addon_sourceURL": "https://github.com/jasonpython50/referenceStyler",
	# Documentation file name
	"addon_docFileName": "readme.html",
	# Minimum NVDA version supported
	"addon_minimumNVDAVersion": "2023.3",
	# Last NVDA version supported/tested
	"addon_lastTestedNVDAVersion": "2024.1",
	# Add-on update channel (default is None, denoting stable releases)
	"addon_updateChannel": None,
	# Add-on license such as GPL 2
	"addon_license": "GPL v2",
	# URL for the license document the add-on is licensed under
	"addon_licenseURL": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
}

# Define the python files that are the sources of your add-on.
# You can either list every file (using ""/") as a path separator,
# or use glob expressions.
# For example to include all files with a ".py" extension from the "globalPlugins" dir of your add-on
# the list can be written as follows:
pythonSources = ["addon/globalPlugins/referenceStyler/*.py"]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []

# Base language for the NVDA add-on
baseLanguage = "en"

# Markdown extensions for add-on documentation
markdownExtensions = []

# Custom braille translation tables
brailleTables = {}