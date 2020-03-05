import tkinter as tk


class WindowActionContainer(tk.Frame):
    def __init__(self, change_handler, master=None):
        super().__init__(master)
        self.window_action_option = tk.StringVar(value="None")
        self.window_action_option.trace("w", change_handler)
        tk.Label(master=self, text="The action...",).pack()
        self.create_radio_buttons()
        self.pack()

    def create_radio_buttons(self):
        tk.Radiobutton(
            master=self,
            text="Restore window(s)",
            variable=self.window_action_option,
            value="Restore",
        ).pack()
        tk.Radiobutton(
            master=self,
            text="Maximize window(s)",
            variable=self.window_action_option,
            value="Maximize",
        ).pack()
        tk.Radiobutton(
            self,
            text="Minimize window(s)",
            variable=self.window_action_option,
            value="Minimize",
        ).pack()

    def get_selection(self):
        if self.window_action_option.get() == "None":
            return None
        return self.window_action_option.get()
