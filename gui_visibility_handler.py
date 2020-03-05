from keyboard import add_hotkey


class GUIVisibilityHandler:
    def __init__(self, gui_root, hotkey_str, gui_is_visible=True):
        self.gui_is_visible = gui_is_visible
        self.gui_root = gui_root
        add_hotkey(hotkey_str, self.toggle_gui_visibility)

    def toggle_gui_visibility(self):
        if self.gui_is_visible:
            self.gui_root.withdraw()
            self.gui_is_visible = False
        else:
            self.gui_root.deiconify()
            self.gui_is_visible = True
