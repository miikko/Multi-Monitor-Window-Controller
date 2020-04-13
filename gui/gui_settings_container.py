import tkinter as tk


class GUISettingsContainer(tk.Frame):
    def __init__(self, gui_settings_manager, master):
        super().__init__(master)
        self.gui_settings_manager = gui_settings_manager
        self.gui_visible_on_start_var = tk.BooleanVar()
        self.gui_visible_on_start_var.set(
            gui_settings_manager.get_gui_start_visibility()
        )
        self.create_widgets()
        self.gui_visible_on_start_var.trace(
            "w", self.tk_var_change_handler
        )

    def create_widgets(self):
        tk.Label(self, text="Show GUI on start").grid(row=0, column=2)
        tk.Radiobutton(
            self,
            text="YES",
            variable=self.gui_visible_on_start_var,
            value=True,
        ).grid(row=1, column=1)
        tk.Radiobutton(
            self,
            text="NO",
            variable=self.gui_visible_on_start_var,
            value=False,
        ).grid(row=1, column=3)

    def tk_var_change_handler(self, *args):
        self.gui_settings_manager.modify_gui_start_visibility(
            self.gui_visible_on_start_var.get()
        )
        self.gui_settings_manager.save_settings()
