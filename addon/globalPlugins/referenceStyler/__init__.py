import globalPluginHandler
import api
import ui
import scriptHandler
from logHandler import log
import threading
import wx
import textInfos
import winUser
import keyboardHandler
import time
import tones
import queueHandler
from NVDAObjects.behaviors import EditableText
from .reference import Reference, ReferenceManager
from .dialogs import show_reference_dialog, show_reference_manager_dialog

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.reference_manager = ReferenceManager()
        self.selected_reference_index = 0
        log.info("ReferenceStyler plugin initialized")

    @scriptHandler.script(
        description="Open Reference Manager",
        gesture="kb:NVDA+shift+f"
    )
    def script_open_reference_manager(self, gesture):
        log.info("Attempting to show reference manager dialog")
        threading.Thread(target=self._show_reference_manager_dialog).start()
        
    def _show_reference_manager_dialog(self):
        try:
            wx.CallAfter(self._show_manager_dialog_in_main_thread)
        except Exception as e:
            log.error(f"Error in _show_reference_manager_dialog: {e}", exc_info=True)

    def _show_manager_dialog_in_main_thread(self):
        try:
            show_reference_manager_dialog(self.reference_manager)
        except Exception as e:
            log.error(f"Error in _show_manager_dialog_in_main_thread: {e}", exc_info=True)

    @scriptHandler.script(
        description="Insert APA style reference",
        gesture="kb:NVDA+shift+a"
    )
    def script_insert_apa(self, gesture):
        self._handle_reference("apa")

    @scriptHandler.script(
        description="Insert MLA style reference",
        gesture="kb:NVDA+shift+m"
    )
    def script_insert_mla(self, gesture):
        self._handle_reference("mla")

    @scriptHandler.script(
        description="Insert Chicago style reference",
        gesture="kb:NVDA+shift+c"
    )
    def script_insert_chicago(self, gesture):
        self._handle_reference("chicago")

    @scriptHandler.script(
        description="Insert Vancouver style reference",
        gesture="kb:NVDA+shift+v"
    )
    def script_insert_vancouver(self, gesture):
        self._handle_reference("vancouver")

    @scriptHandler.script(
        description="Insert Harvard style reference",
        gesture="kb:NVDA+shift+h"
    )
    def script_insert_harvard(self, gesture):
        self._handle_reference("harvard")

    @scriptHandler.script(
        description="Insert IEEE style reference",
        gesture="kb:NVDA+shift+i"
    )
    def script_insert_ieee(self, gesture):
        self._handle_reference("ieee")

    @scriptHandler.script(
        description="Insert AMA style reference",
        gesture="kb:NVDA+shift+d"
    )
    def script_insert_ama(self, gesture):
        self._handle_reference("ama")

    @scriptHandler.script(
        description="Insert ACS style reference",
        gesture="kb:NVDA+shift+e"
    )
    def script_insert_acs(self, gesture):
        self._handle_reference("acs")

    def _handle_reference(self, style):
        if not self.reference_manager.references:
            ui.message("No references available. Please add a reference first.")
            return

        if self.selected_reference_index >= len(self.reference_manager.references):
            ui.message("Invalid reference selection. Please select a reference first.")
            return

        reference = self.reference_manager.references[self.selected_reference_index]
        formatted_reference = getattr(reference, f"format_{style}")()
        
        # Copy the reference to clipboard
        api.copyToClip(formatted_reference)
        
        focus = api.getFocusObject()
        if isinstance(focus, EditableText):
            self._insert_reference(formatted_reference, style)
        else:
            ui.message(f"{style.upper()} style reference copied to clipboard. Not in an editable field.")

    def _insert_reference(self, formatted_reference, style):
        try:
            # Press Ctrl
            winUser.keybd_event(winUser.VK_CONTROL, 0, 0, 0)
            # Press V
            winUser.keybd_event(ord('V'), 0, 0, 0)
            # Release V
            winUser.keybd_event(ord('V'), 0, winUser.KEYEVENTF_KEYUP, 0)
            # Release Ctrl
            winUser.keybd_event(winUser.VK_CONTROL, 0, winUser.KEYEVENTF_KEYUP, 0)
            
            # Give some time for the paste operation to complete
            time.sleep(0.3)
            
            # Play a success sound
            tones.beep(1000, 50)
            
            # Report success after a short delay
            queueHandler.queueFunction(queueHandler.eventQueue, ui.message, f"{style.upper()} style reference inserted")
        except:
            ui.message(f"Cannot insert text at the current position. {style.upper()} style reference is copied to clipboard.")

    @scriptHandler.script(
        description="Select reference to insert",
        gesture="kb:NVDA+shift+s"
    )
    def script_select_reference(self, gesture):
        if not self.reference_manager.references:
            ui.message("No references available. Please add a reference first.")
            return
        
        references = [f"{ref.authors} ({ref.year}): {ref.title}" for ref in self.reference_manager.references]
        
        wx.CallAfter(self._show_reference_selection_dialog, references)

    def _show_reference_selection_dialog(self, references):
        def showDialog():
            dialog = wx.SingleChoiceDialog(None, "Select a reference", "Reference Selection", references)
            if dialog.ShowModal() == wx.ID_OK:
                self.selected_reference_index = dialog.GetSelection()
                wx.CallAfter(lambda: ui.message(f"Selected: {references[self.selected_reference_index]}"))
            else:
                wx.CallAfter(lambda: ui.message("No reference selected"))
            dialog.Destroy()
        
        wx.CallAfter(showDialog)

    def terminate(self):
        super(GlobalPlugin, self).terminate()