import wx
import gui
from logHandler import log
from .reference import Reference

class ReferenceDialog(wx.Dialog):
    def __init__(self, parent):
        super(ReferenceDialog, self).__init__(parent, title="Enter Reference")
        self.create_controls()

    def create_controls(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        fields = [
            ("Authors:", "authors"), ("Year:", "year"), ("Title:", "title"), ("Source:", "source"),
            ("URL:", "url"), ("Editor:", "editor"), ("Translator:", "translator"),
            ("Edition:", "edition"), ("Volume:", "volume"), ("Issue:", "issue"),
            ("Pages:", "pages"), ("Publisher:", "publisher"), ("Publication Date:", "publication_date"),
            ("Place of Publication:", "place_of_publication"), ("DOI:", "doi"),
            ("Access Date:", "access_date"), ("ISBN/ISSN:", "isbn_issn"),
            ("Conference Name:", "conference_name"), ("Database:", "database"),
            ("Medium:", "medium"), ("Institution:", "institution"), ("Series Title:", "series_title"),
            ("Contributors:", "contributors"), ("Chapter Title:", "chapter_title"),
            ("Original Publication Date:", "original_publication_date"), ("Review:", "review"),
            ("Lecture Title:", "lecture_title"), ("Thesis Type:", "thesis_type"),
            ("Patent Number:", "patent_number")
        ]
        self.text_ctrls = {}

        scrolled_window = wx.ScrolledWindow(panel, style=wx.VSCROLL)
        scrolled_sizer = wx.BoxSizer(wx.VERTICAL)

        for label, name in fields:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            hsizer.Add(wx.StaticText(scrolled_window, label=label), 0, wx.ALL, 5)
            self.text_ctrls[name] = wx.TextCtrl(scrolled_window)
            hsizer.Add(self.text_ctrls[name], 1, wx.EXPAND|wx.ALL, 5)
            scrolled_sizer.Add(hsizer, 0, wx.EXPAND)

        scrolled_window.SetSizer(scrolled_sizer)
        scrolled_window.SetScrollRate(0, 10)

        sizer.Add(scrolled_window, 1, wx.EXPAND|wx.ALL, 5)

        btn_sizer = wx.StdDialogButtonSizer()
        btn_sizer.AddButton(wx.Button(panel, wx.ID_OK))
        btn_sizer.AddButton(wx.Button(panel, wx.ID_CANCEL))
        btn_sizer.Realize()
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        panel.SetSizer(sizer)
        sizer.Fit(self)
        self.SetSize((500, 600))  # Set a fixed size for the dialog

    def get_data(self):
        return {name: ctrl.GetValue() for name, ctrl in self.text_ctrls.items()}

class ReferenceManagerDialog(wx.Dialog):
    def __init__(self, parent, reference_manager):
        super(ReferenceManagerDialog, self).__init__(parent, title="Reference Manager")
        self.reference_manager = reference_manager
        self.create_controls()

    def create_controls(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.reference_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.update_reference_list()
        sizer.Add(self.reference_list, 1, wx.EXPAND|wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_btn = wx.Button(panel, label="Add")
        add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        btn_sizer.Add(add_btn, 0, wx.ALL, 5)

        remove_btn = wx.Button(panel, label="Remove")
        remove_btn.Bind(wx.EVT_BUTTON, self.on_remove)
        btn_sizer.Add(remove_btn, 0, wx.ALL, 5)

        save_btn = wx.Button(panel, label="Save")
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        btn_sizer.Add(save_btn, 0, wx.ALL, 5)

        load_btn = wx.Button(panel, label="Load")
        load_btn.Bind(wx.EVT_BUTTON, self.on_load)
        btn_sizer.Add(load_btn, 0, wx.ALL, 5)

        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)

        close_btn = wx.Button(panel, wx.ID_CLOSE)
        close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.ID_CLOSE))
        sizer.Add(close_btn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        panel.SetSizer(sizer)
        sizer.Fit(self)

    def update_reference_list(self):
        self.reference_list.Clear()
        for ref in self.reference_manager.references:
            self.reference_list.Append(f"{ref.authors} ({ref.year}) - {ref.title}")

    def on_add(self, event):
        with ReferenceDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.get_data()
                reference = Reference(**data)
                self.reference_manager.add_reference(reference)
                self.update_reference_list()

    def on_remove(self, event):
        selection = self.reference_list.GetSelection()
        if selection != wx.NOT_FOUND:
            self.reference_manager.remove_reference(selection)
            self.update_reference_list()

    def on_save(self, event):
        with wx.FileDialog(self, "Save references", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            self.reference_manager.save_to_file(pathname)

    def on_load(self, event):
        with wx.FileDialog(self, "Load references", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            self.reference_manager.load_from_file(pathname)
            self.update_reference_list()

def show_reference_dialog():
    log.info("Entering show_reference_dialog")
    if not wx.GetApp():
        log.info("Creating wx.App")
        app = wx.App()
    try:
        with ReferenceDialog(gui.mainFrame) as dlg:
            log.info("Dialog created")
            result = dlg.ShowModal()
            log.info(f"Dialog result: {result}")
            if result == wx.ID_OK:
                return dlg.get_data()
    except Exception as e:
        log.error(f"Error in show_reference_dialog: {e}", exc_info=True)
    finally:
        log.info("Exiting show_reference_dialog")
    return None

def show_reference_manager_dialog(reference_manager):
    log.info("Entering show_reference_manager_dialog")
    if not wx.GetApp():
        log.info("Creating wx.App")
        app = wx.App()
    try:
        with ReferenceManagerDialog(gui.mainFrame, reference_manager) as dlg:
            log.info("Dialog created")
            result = dlg.ShowModal()
            log.info(f"Dialog result: {result}")
    except Exception as e:
        log.error(f"Error in show_reference_manager_dialog: {e}", exc_info=True)
    finally:
        log.info("Exiting show_reference_manager_dialog")