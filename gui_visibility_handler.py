from keyboard import add_hotkey
from threading import Thread
from gui.sys_tray_icon import SysTrayIcon


class GUIVisibilityHandler:
    def __init__(self, gui_root, hotkey_str, gui_is_visible=True):
        self.gui_is_visible = gui_is_visible
        self.gui_root = gui_root
        self.icon_thread = Thread(
            target=self.create_sys_tray_icon, daemon=True
        )
        self.icon_thread.start()
        add_hotkey(hotkey_str, self.toggle_gui_visibility)

    def toggle_gui_visibility(self):
        if self.gui_is_visible:
            self.hide_gui()
        else:
            self.display_gui()

    def display_gui(self):
        self.gui_root.deiconify()
        self.gui_is_visible = True

    def hide_gui(self):
        self.gui_root.withdraw()
        self.gui_is_visible = False

    def create_sys_tray_icon(self):
        SysTrayIcon(
            "application_icon.ico",
            "Multi-Monitor Window controller",
            menu_options=(("Show GUI", None, self.display_gui),),
            default_menu_index=1,
        )
        # After Quit is pressed from tray icon menu
        self.gui_root.destroy()
